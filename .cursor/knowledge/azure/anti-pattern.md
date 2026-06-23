# Azure Knowledge Base - Anti-Patterns

## Tổng quan

Document này liệt kê các anti-patterns phổ biến khi sử dụng Azure và đề xuất giải pháp thay thế. Mỗi anti-pattern được mô tả chi tiết với ví dụ về cách phát hiện và khắc phục.

## Anti-Pattern 1: Using Admin Credentials Directly in Code

### Mô tả

Hardcoding credentials trong code là security risk nghiêm trọng. Credentials có thể bị exposed qua source control, logs, hoặc network traffic.

### Ví dụ xấu

```typescript
// ❌ ANTI-PATTERN: Hardcoded credentials
const connectionString = "DefaultEndpointsProtocol=https;AccountName=mystorage;AccountKey=abcdef123456==";

const client = new StorageClient(connectionString);

// Or worse
const subscriptionId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx";
const clientId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx";
const clientSecret = "supersecretpassword";
```

### Giải pháp

```typescript
// ✅ SOLUTION: Use Managed Identity
import { DefaultAzureCredential } from "@azure/identity";

async function connectToStorage() {
  const credential = new DefaultAzureCredential();
  
  // Azure SDK uses managed identity automatically
  const { token } = await credential.getToken(
    "https://storage.azure.com/.default"
  );
  
  return token;
}

// ✅ SOLUTION: Use Key Vault reference in App Service
// In Application Settings:
// Azure Key Vault references: @Microsoft.KeyVault(SecretUri={secret-uri})

// ✅ SOLUTION: Environment variables with Key Vault
import { SecretClient } from "@azure/keyvault-secrets";
import { DefaultAzureCredential } from "@azure/identity";

async function getSecrets() {
  const credential = new DefaultAzureCredential();
  const client = new SecretClient(
    "https://myKeyVault.vault.azure.net/",
    credential
  );
  
  const connectionString = await client.getSecret("ConnectionString");
  return connectionString.value;
}
```

## Anti-Pattern 2: Not Using Resource Tags

### Mô tả

Không tag resources dẫn đến khó khăn trong cost tracking, resource management, và compliance reporting.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: No tags
az group create --name myRG --location eastus
az vm create --resource-group myRG --name myVM --image UbuntuLTS

# Later, tracking costs is impossible
az cost management query \
  --resource-group myRG
# No tag data to filter by!
```

### Giải pháp

```bash
# ✅ SOLUTION: Tag everything
az group update --name myRG \
  --set tags.Environment=Production tags.Team=Platform tags.CostCenter=CC-1234 tags.Project=MyApp

az vm create --resource-group myRG --name myVM --image UbuntuLTS \
  --tags Environment=Production Team=Platform CostCenter=CC-1234 Project=MyApp

# Azure Policy to enforce tags
az policy definition create \
  --name "require-tags" \
  --display-name "Require tags on resources" \
  --rules '{
    "if": {
      "not": {
        "field": "tags",
        "containsKey": "Environment"
      }
    },
    "then": {
      "effect": "deny"
    }
  }'
```

```json
// ✅ Tagging policy in ARM template
{
  "resources": [
    {
      "type": "Microsoft.Compute/virtualMachines",
      "apiVersion": "2023-03-01",
      "tags": {
        "Environment": "[parameters('environment')]",
        "Team": "[parameters('team')]",
        "CostCenter": "[parameters('costCenter')]"
      }
    }
  ]
}
```

## Anti-Pattern 3: Not Using Availability Zones

### Mô tả

Deploying resources in a single availability zone creates single point of failure. Zone-wide outages can take down entire application.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: No availability zone specification
az vm create \
  --resource-group myRG \
  --name myVM \
  --location eastus \
  # No --availability-zone specified!
```

### Giải pháp

```bash
# ✅ SOLUTION: Deploy across availability zones
az vm create \
  --resource-group myRG \
  --name myVM1 \
  --location eastus \
  --availability-zone 1

az vm create \
  --resource-group myRG \
  --name myVM2 \
  --location eastus \
  --availability-zone 2

az vm create \
  --resource-group myRG \
  --name myVM3 \
  --location eastus \
  --availability-zone 3

# ✅ SOLUTION: Use zone-redundant SQL
az sql db create \
  --resource-group myRG \
  --server myserver \
  --name myDatabase \
  --zone-redundant true
```

```yaml
# ✅ AKS with availability zones
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
    - port: 80
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
  template:
    spec:
      topologyologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: myapp
```

## Anti-Pattern 4: Not Configuring Proper Logging

### Mô tả

Không enable logging và monitoring dẫn đến không có visibility vào application health và security events.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: Create resources without diagnostics
az storage account create \
  --resource-group myRG \
  --name mystorageaccount

# No diagnostic settings - no logs!
```

### Giải pháp

```bash
# ✅ SOLUTION: Enable comprehensive logging
# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --resource-group myRG \
  --workspace-name myWorkspace

# Enable diagnostics on storage account
az monitor diagnostic-settings create \
  --resource /subscriptions/{sub-id}/resourceGroups/myRG/providers/Microsoft.Storage/storageAccounts/mystorageaccount \
  --workspace myWorkspace \
  --logs '[
    {
      "category": "StorageRead",
      "enabled": true
    },
    {
      "category": "StorageWrite",
      "enabled": true
    },
    {
      "category": "StorageDelete",
      "enabled": true
    }
  ]' \
  --metrics '[
    {
      "category": "AllMetrics",
      "enabled": true
    }
  ]'

# Enable Azure Monitor for AKS
az aks enable-addons \
  --resource-group myRG \
  --name myAKS \
  --addons monitoring
```

## Anti-Pattern 5: Using Premium Storage for Everything

### Mô tả

Overprovisioning storage tier dẫn đến unnecessary costs. Not all workloads need premium SSD.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: Premium storage for development
az storage account create \
  --resource-group myRG \
  --name mystorageaccount \
  --sku Premium_LRS  # Too expensive for dev!

az vm create \
  --resource-group myRG \
  --name myVM \
  --size Standard_D2s_v3 \
  --managed-disk-type Premium_LRS  # Unnecessary for dev!
```

### Giải pháp

```bash
# ✅ SOLUTION: Match storage tier to workload
# Development - Standard tier
az storage account create \
  --resource-group devRG \
  --name devstorageaccount \
  --sku Standard_LRS

# Production - Premium for VMs, Standard for storage
az storage account create \
  --resource-group prodRG \
  --name prodstorageaccount \
  --sku Standard_GRS  # Geo-redundant for production

az vm create \
  --resource-group prodRG \
  --name myVM \
  --size Standard_D8s_v3 \
  --managed-disk-type Premium_LRS  # Only for production VMs

# Database - use appropriate tier
az sql db create \
  --resource-group myRG \
  --server myserver \
  --name myDatabase \
  --service-objective S0  # Start small, scale up as needed
```

## Anti-Pattern 6: Not Using Azure Policy

### Mô tả

Without Azure Policy, teams can create resources that don't meet organizational standards, leading to security gaps và cost overruns.

### Ví� dụ xấu

```bash
# ❌ ANTI-PATTERN: No governance
# Anyone can create expensive resources
az vm create --size Standard_E64s_v3 --name expensiveVM  # No cost control!
az storage account create --sku Premium_LRS --name premium  # No standard enforcement!
```

### Giải phól

```bash
# ✅ SOLUTION: Implement Azure Policy
# Allowed VM sizes
az policy definition create \
  --name "allowed-vm-sizes" \
  --display-name "Allowed VM sizes" \
  --rules '{
    "if": {
      "allOf": [
        {
          "field": "type",
          "equals": "Microsoft.Compute/virtualMachines"
        },
        {
          "not": {
            "field": "Microsoft.Compute/virtualMachines/sku.name",
            "in": ["Standard_D2s_v3", "Standard_D4s_v3", "Standard_D8s_v3"]
          }
        }
      ]
    },
    "then": {
      "effect": "Deny"
    }
  }'

# Require encryption
az policy definition create \
  --name "require-storage-encryption" \
  --display-name "Require storage encryption" \
  --rules '{
    "if": {
      "field": "type",
      "equals": "Microsoft.Storage/storageAccounts"
    },
    "then": {
      "effect": "Deny",
      "details": {
        "operation": "Microsoft.Storage/storageAccounts/write"
      }
    }
  }'

# Assign policies at management group level
az policy assignment create \
  --name "org-policy-assignment" \
  --scope /providers/Microsoft.Management/managementGroups/myMG \
  --policy "allowed-vm-sizes"
```

## Anti-Pattern 7: Not Planning for Scalability

### Mô tả

Single-instance deployments không scale được và có single point of failure.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: Single instance
az appservice plan create \
  --resource-group myRG \
  --name myAppServicePlan \
  --sku B1  # Single instance!

az webapp create \
  --resource-group myRG \
  --name myWebApp \
  --plan myAppServicePlan
```

### Giải pháp

```bash
# ✅ SOLUTION: Plan for scalability
# App Service with auto-scaling
az appservice plan create \
  --resource-group myRG \
  --name myAppServicePlan \
  --sku S1  # Standard tier for scaling

az appservice plan update \
  --resource-group myRG \
  --name myAppServicePlan \
  --min-instances 2 \
  --max-instances 10

# Enable auto-scale
az monitor autoscale create \
  --resource-group myRG \
  --resource myAppServicePlan \
  --resource-type Microsoft.Web/serverfarms \
  --name myAutoscaleSettings

# AKS with autoscaling
az aks update \
  --resource-group myRG \
  --name myAKS \
  --enable-cluster-autoscaler \
  --min-count 3 \
  --max-count 10
```

## Anti-Pattern 8: Not Using Private Endpoints

### Mô tả

Exposing storage, databases, và other services to public internet increases attack surface.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: Public endpoints
az storage account create \
  --resource-group myRG \
  --name mystorageaccount \
  --public-network-access Enabled  # Public access!

az sql server create \
  --resource-group myRG \
  --name myserver \
  --public-network-access Enabled  # Public access!
```

### Giải pháp

```bash
# ✅ SOLUTION: Use private endpoints
# Disable public access on storage
az storage account update \
  --resource-group myRG \
  --name mystorageaccount \
  --public-network-access Disabled

# Create private endpoint for storage
az network private-endpoint create \
  --resource-group myRG \
  --name myStoragePE \
  --vnet-name myVNet \
  --subnet mySubnet \
  --private-connection-resource-id $(az storage account show --name mystorageaccount --query id --output tsv) \
  --connection-name myStorageConnection \
  --group-id blob

# Create private DNS zone for storage
az network private-dns zone create \
  --resource-group myRG \
  --name privatelink.blob.core.windows.net

az network private-dns link vnet create \
  --resource-group myRG \
  --zone-name privatelink.blob.core.windows.net \
  --name myDnsLink \
  --virtual-network myVNet \
  --registration-enabled false

# Create DNS A record
az network private-dns record-set a create \
  --resource-group myRG \
  --zone-name privatelink.blob.core.windows.net \
  --name mystorageaccount \
  --ttl 300

az network private-dns record-set a show \
  --resource-group myRG \
  --zone-name privatelink.blob.core.windows.net \
  --name mystorageaccount
```

## Anti-Pattern 9: Not Implementing Backup Strategy

### Mô tả

Without backup, data loss can be catastrophic. Ransomware, accidental deletion, hoặc application bugs can destroy data.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: No backup
az sql db create \
  --resource-group myRG \
  --server myserver \
  --name myDatabase
# No backup policy - data at risk!
```

### Giải pháp

```bash
# ✅ SOLUTION: Implement comprehensive backup
# Create Recovery Services vault
az backup vault create \
  --resource-group myRG \
  --name myRecoveryVault \
  --location eastus

# Enable backup for VMs
az backup protection enable-for-vm \
  --resource-group myRG \
  --vault-name myRecoveryVault \
  --vm myVM \
  --policy-name DefaultPolicy

# Enable point-in-time restore for SQL
az sql db update \
  --resource-group myRG \
  --server myserver \
  --name myDatabase \
  --backup-storage-redundancy Geo

# Configure Azure SQL auto-backup
az sql db auto-punctuation update \
  --resource-group myRG \
  --server myserver \
  --name myDatabase \
  --retention-days 30

# Enable soft delete for blobs
az storage account blob-service-properties update \
  --resource-group myRG \
  --account-name mystorageaccount \
  --enable-delete-retention true \
  --delete-retention-days 30
```

## Anti-Pattern 10: Not Using Managed Disks

### Mô tả

Using unmanaged disks requires manual management of storage accounts, leading to complexity và potential bottlenecks.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: Unmanaged disks
az vm create \
  --resource-group myRG \
  --name myVM \
  --use-unmanaged-disk \
  --storage-account mystorageaccount
# Storage account becomes bottleneck!
# Manual storage account management required!
```

### Giải pháp

```bash
# ✅ SOLUTION: Use managed disks
az vm create \
  --resource-group myRG \
  --name myVM \
  --os-disk-size-gb 128 \
  --os-disk-encryption-set myEncryptionSet \
  --disk-encryption-set-resource-group myRG

# Configure disk redundancy
az disk create \
  --resource-group myRG \
  --name myDisk \
  --sku StandardSSD_LRS \
  --size-gb 100

# Enable disk redundancy
az disk update \
  --resource-group myRG \
  --name myDisk \
  --sku Premium_ZRS  # Zone-redundant for production
```

## Anti-Pattern 11: Not Using Azure Bastion

### Mô tả

Exposing VMs via public RDP/SSH ports creates security risk. Direct access to VMs should be avoided.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: Public SSH/RDP
az vm create \
  --resource-group myRG \
  --name myVM \
  --public-ip-address myPublicIP

# Then enable SSH on port 22 - SECURITY RISK!
```

### Giải pháp

```bash
# ✅ SOLUTION: Use Azure Bastion
# Create Bastion host
az bastion create \
  --resource-group myRG \
  --name myBastion \
  --vnet-name myVNet \
  --subnet-name AzureBastionSubnet

# No public IP needed for VMs!
az vm create \
  --resource-group myRG \
  --name myVM \
  --public-ip-address ""  # No public IP

# Or remove existing public IPs
az network public-ip delete --name myPublicIP --resource-group myRG

# Connect via Bastion in Azure Portal
# Or via CLI
az bastion show --resource-group myRG --name myBastion
```

## Related Documents

- [Azure Glossary](../glossary.md)
- [Azure Architecture](../architecture.md)
- [Azure Best Practices](../best-practice.md)
- [Azure Checklist](../checklist.md)
- [Azure FAQ](../faq.md)
- [Azure Decision Tree](../decision-tree.md)
