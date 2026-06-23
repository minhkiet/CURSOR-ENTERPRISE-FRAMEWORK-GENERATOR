# Azure Knowledge Base - FAQ

## Tổng quan

Document này cung cấp 10 câu hỏi thường gặp và câu trả lời chi tiết về Azure trong Cursor Enterprise Framework.

## Câu hỏi 1: Làm thế nào để bắt đầu với Azure?

### Câu trả lời

```bash
# 1. Đăng ký Azure account
# Truy cập https://azure.microsoft.com/free để đăng ký

# 2. Cài đặt Azure CLI
# Windows: winget install Microsoft.AzureCLI
# macOS: brew install azure-cli
# Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# 3. Đăng nhập
az login

# 4. Thiết lập subscription
az account list --output table
az account set --subscription "subscription-name-or-id"

# 5. Tạo resource group đầu tiên
az group create --name myResourceGroup --location eastus

# 6. Tạo resources đầu tiên
# Virtual Network
az network vnet create \
  --resource-group myResourceGroup \
  --name myVNet \
  --address-prefix 10.0.0.0/16

# Virtual Machine
az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys

# 7. Clean up
az group delete --name myResourceGroup --yes
```

### Các bước tiếp theo

1. **Learn Azure Fundamentals**: Xem Microsoft Learn courses
2. **Practice with Free Account**: Sử dụng $200 credit trong 30 ngày
3. **Deploy First Application**: Sử dụng App Service hoặc AKS
4. **Implement Security**: Enable Azure AD, configure RBAC
5. **Set up Monitoring**: Azure Monitor, Application Insights

## Câu hỏi 2: Sự khác biệt giữa các Azure services là gì?

### Câu trả lời

| Service | Use Case | Type |
|---------|----------|------|
| Azure VMs | Full control over OS | IaaS |
| App Service | Web apps, APIs | PaaS |
| Azure Functions | Event-driven, serverless | FaaS |
| AKS | Container orchestration | PaaS |
| Azure Container Instances | Containers without orchestration | PaaS |
| Azure Batch | HPC, batch computing | PaaS |

```bash
# Quick decision guide:

# Need full OS control? → Azure VMs
az vm create --resource-group myRG --name myVM --image UbuntuLTS

# Need to host web app/API? → App Service
az appservice plan create --resource-group myRG --name myPlan --sku B1
az webapp create --resource-group myRG --name myWebApp --plan myPlan

# Need serverless functions? → Azure Functions
az functionapp create --resource-group myRG --name myFunction --consumption-plan

# Need Kubernetes? → AKS
az aks create --resource-group myRG --name myAKS --node-count 3
```

## Câu hỏi 3: Làm thế nào để secure Azure resources?

### Câu trả lời

```bash
# 1. Enable Azure AD và MFA
# Truy cập Azure Portal > Azure Active Directory

# 2. Use Managed Identity thay vì credentials
az webapp identity assign --resource-group myRG --name myWebApp

# 3. Store secrets in Key Vault
az keyvault create --resource-group myRG --name myKeyVault
az keyvault secret set --vault-name myKeyVault --name "DbPassword" --value "secret"

# 4. Configure RBAC
az role assignment create \
  --assignee user@example.com \
  --role "Reader" \
  --scope /subscriptions/{sub-id}/resourceGroups/myRG

# 5. Use Network Security Groups
az network nsg create --resource-group myRG --name myNSG
az network nsg rule create \
  --resource-group myRG \
  --nsg-name myNSG \
  --name AllowHTTPS \
  --priority 100 \
  --source-address-prefixes Internet \
  --destination-port-ranges 443 \
  --access Allow

# 6. Enable DDoS Protection
az network ddos-protection create \
  --resource-group myRG \
  --name myDDOSProtection \
  --vnets myVNet

# 7. Enable Azure Security Center
az security pricing create -n default --tier standard
```

```typescript
// Access Key Vault in code
import { SecretClient } from "@azure/keyvault-secrets";
import { DefaultAzureCredential } from "@azure/identity";

async function getSecret(secretName: string) {
  const credential = new DefaultAzureCredential();
  const client = new SecretClient(
    "https://myKeyVault.vault.azure.net/",
    credential
  );
  
  const secret = await client.getSecret(secretName);
  return secret.value;
}
```

## Câu hỏi 4: Làm thế nào để reduce Azure costs?

### Câu trả lời

```bash
# 1. Right-size resources
az vm list-sizes --location eastus --output table

# Resize underutilized VM
az vm stop --resource-group myRG --name myVM
az vm resize --resource-group myRG --name myVM --size Standard_D2s_v3

# 2. Use Reserved Instances
az reservedvminstances purchase \
  --reserved-vm-size Standard_D2s_v3 \
  --term 1 \
  --quantity 3

# 3. Enable auto-shutdown for dev VMs
az vm auto-shutdown \
  --resource-group myRG \
  --name myDevVM \
  --time 1900  # 7PM UTC

# 4. Use managed disks appropriately
# Development: Standard HDD
az disk create --resource-group myRG --name myDisk --sku Standard_LRS

# Production: Premium SSD
az disk create --resource-group myRG --name myDisk --sku Premium_LRS

# 5. Use Azure Policy to enforce cost controls
az policy definition create \
  --name "deny-premium-storage" \
  --display-name "Deny premium storage for dev" \
  --rules '{
    "if": {
      "allOf": [
        {"field": "type", "equals": "Microsoft.Compute/disks"},
        {"field": "tags.Environment", "notEquals": "Production"}
      ]
    },
    "then": {
      "effect": "deny",
      "details": {
        "name": "SkuName",
        "operator": "Equals",
        "value": "Premium_LRS"
      }
    }
  }'

# 6. Set up budget alerts
az costmanagement budget create \
  --resource-group myRG \
  --name myBudget \
  --amount 1000 \
  --time-grain Monthly

# 7. Delete unused resources
az resource list --tag "delete=true" --query [].name
az group delete --name unused-rg --yes
```

## Câu hỏi 5: Làm thế nào để monitor Azure resources?

### Câu trả lời

```bash
# 1. Create Log Analytics workspace
az monitor log-analytics workspace create \
  --resource-group myRG \
  --workspace-name myWorkspace

# 2. Enable diagnostics for resources
az monitor diagnostic-settings create \
  --resource myStorageAccount \
  --workspace myWorkspace \
  --logs '[
    {"category": "StorageRead", "enabled": true},
    {"category": "StorageWrite", "enabled": true}
  ]' \
  --metrics '[
    {"category": "AllMetrics", "enabled": true}
  ]'

# 3. Create alerts
az monitor alert create \
  --resource-group myRG \
  --name cpuAlert \
  --target myVM \
  --condition "Percentage CPU > 80" \
  --time-aggregation Average \
  --window-size 5m

# 4. Enable Application Insights
az resource create \
  --resource-group myRG \
  --name myAppInsights \
  --type "Microsoft.Insights/components" \
  --properties '{"Application_Type":"web"}'

# 5. Create dashboard
az dashboard create \
  --resource-group myRG \
  --name myDashboard \
  --location eastus
```

```typescript
// Application Insights in code
import { ApplicationInsights } from "@microsoft/applicationinsights-web";

const appInsights = new ApplicationInsights({
  config: {
    connectionString: process.env.APPINSIGHTS_CONNECTIONSTRING,
    enableAutoRouteTracking: true
  }
});

appInsights.loadAppInsights();

// Track custom metrics
appInsights.trackMetric({
  name: "RequestDuration",
  value: requestDuration,
  properties: {
    endpoint: request.url,
    statusCode: response.status
  }
});
```

## Câu hỏi 6: Azure Storage có các loại nào và khi nào nên sử dụng?

### Câu trả lời

| Storage Type | Use Case | Performance |
|------------|----------|-------------|
| Blob Storage | Unstructured data (images, videos, files) | Scalable |
| Azure Files | SMB/NFS file shares | Enterprise |
| Queue Storage | Async messaging | Simple |
| Table Storage | NoSQL (structured data) | Scalable |
| Disk Storage | VM disks | High IOPS |

```bash
# Create Storage Account
az storage account create \
  --resource-group myRG \
  --name mystorageaccount \
  --sku Standard_GRS \
  --kind StorageV2

# Blob Storage - for static website hosting
az storage container create \
  --name $web \
  --account-name mystorageaccount \
  --public-access blob

az storage blob upload-batch \
  --source ./www \
  --destination https://mystorageaccount.blob.core.windows.net/$web

# Enable static website
az storage account update \
  --resource-group myRG \
  --name mystorageaccount \
  --static-website

# Azure Files - for shared storage
az storage share create \
  --name myfileshare \
  --account-name mystorageaccount

# Queue Storage - for async processing
az storage queue create \
  --name myqueue \
  --account-name mystorageaccount

az storage queue message put \
  --queue-name myqueue \
  --content "Hello" \
  --account-name mystorageaccount
```

## Câu hỏi 7: Làm thế nào để backup và restore trong Azure?

### Câu trả lời

```bash
# 1. Create Recovery Services vault
az backup vault create \
  --resource-group myRG \
  --name myRecoveryVault \
  --location eastus

# 2. Enable VM backup
az backup protection enable-for-vm \
  --resource-group myRG \
  --vault-name myRecoveryVault \
  --vm myVM \
  --policy-name DefaultPolicy

# 3. Trigger manual backup
az backup protection backup-now \
  --resource-group myRG \
  --vault-name myRecoveryVault \
  --container-name myVM \
  --item-name myVM \
  --retain-until 30-12-2024

# 4. Restore VM
az backup restore restore-disks \
  --resource-group myRG \
  --vault-name myRecoveryVault \
  --container-name myVM \
  --item-name myVM \
  --storage-account mystorageaccount

# 5. Azure SQL backup
az sql db show \
  --resource-group myRG \
  --server myserver \
  --name myDatabase \
  --query "currentBackupRetentionDays"

# Restore point-in-time
az sql db restore \
  --resource-group myRG \
  --server myserver \
  --name myDatabase-restored \
  --source-db-name myDatabase \
  --restore-point-in-time "2024-01-15T12:00:00"
```

## Câu hỏi 8: Làm thế nào để deploy infrastructure as code với Azure?

### Câu trả lời

```bicep
// main.bicep - Infrastructure as Code
param location string = resourceGroup().location
param webAppName string = 'myWebApp-${uniqueString(resourceGroup().id)}'
param appServicePlanSku string = 'B1'

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: '${webAppName}-plan'
  location: location
  sku: {
    name: appServicePlanSku
  }
}

// Web App
resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: webAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'NODE|18-lts'
      appSettings: [
        { name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE', value: 'false' }
      ]
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}

// Key Vault for secrets
resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' = {
  name: '${webAppName}-kv'
  location: location
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
  }
}

// Outputs
output webAppUrl string = webApp.properties.defaultHostName
output keyVaultUri string = keyVault.properties.vaultUri
```

```bash
# Deploy với Azure CLI
az deployment group create \
  --resource-group myRG \
  --template-file main.bicep \
  --parameters webAppName=myApp appServicePlanSku=B1

# Deploy với GitHub Actions
# .github/workflows/deploy.yml
name: Deploy Infrastructure

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
          
      - name: Deploy Bicep
        uses: azure/arm-deploy@v1
        with:
          scope: resourcegroup
          subscriptionId: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          resourceGroupName: myRG
          template: main.bicep
          parameters: main.bicepparam
```

## Câu hỏi 9: Làm thế nào để implement disaster recovery?

### Câu trả lời

```bash
# 1. Configure Azure Site Recovery
az backup vault create \
  --resource-group myRG \
  --name myRecoveryVault \
  --location eastus

# 2. Enable replication for VMs
az site-recovery vault create \
  --resource-group myRG \
  --name mySiteRecoveryVault

# 3. Configure failover
az site-recovery service configure-replication \
  --resource-group myRG \
  --vault-name mySiteRecoveryVault \
  --fabric Azure \
  --protection-container myProtectionContainer \
  --vm-protection-target vm-id \
  --target-resource-group targetRG \
  --target-vnet targetVNet

# 4. Azure SQL Geo-Replication
az sql db replica create \
  --resource-group myRG \
  --server myserver \
  --name myDatabase \
  --partner-resource-group partnerRG \
  --partner-server partnerServer

# 5. Storage Account Geo-Replication
az storage account show-connection-string \
  --name mystorageaccount

# 6. Cosmos DB Multi-region
az cosmosdb create \
  --resource-group myRG \
  --name myCosmosDB \
  --locations eastus=0 westus=1
```

```bash
# Test failover
az site-recovery initate-failover \
  --vault-name mySiteRecoveryVault \
  --fabric-name myFabric \
  --protection-container-name myContainer \
  --recovery-plan-name myPlan \
  --direction PrimaryToRecovery

# Cleanup after test
az site-recovery reprotect \
  --vault-name mySiteRecoveryVault
```

## Câu hỏi 10: Best practices cho Azure Kubernetes Service (AKS)?

### Câu trả lời

```bash
# 1. Create AKS cluster with best practices
az aks create \
  --resource-group myRG \
  --name myAKS \
  --node-count 3 \
  --enable-addons monitoring \
  --enable-azure-defender \
  --enable-cluster-autoscaler \
  --min-count 2 \
  --max-count 10 \
  --network-plugin azure \
  --network-policy azure \
  --enable-rbac \
  --enable-aad

# 2. Use managed identity
az aks update \
  --resource-group myRG \
  --name myAKS \
  --enable-managed-identity

# 3. Enable Azure AD integration
az aks update \
  --resource-group myRG \
  --name myAKS \
  --enable-aad

# 4. Add system node pool
az aks nodepool add \
  --resource-group myRG \
  --cluster-name myAKS \
  --name system \
  --node-count 2 \
  --priority System

# 5. Add user node pool with autoscaling
az aks nodepool add \
  --resource-group myRG \
  --cluster-name myAKS \
  --name user \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 5 \
  --node-vm-size Standard_D2s_v3
```

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      # Use non-root user
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
        - name: myapp
          image: myapp:latest
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
```

## Related Documents

- [Azure Glossary](../glossary.md)
- [Azure Architecture](../architecture.md)
- [Azure Best Practices](../best-practice.md)
- [Azure Anti-Patterns](../anti-pattern.md)
- [Azure Checklist](../checklist.md)
- [Azure Decision Tree](../decision-tree.md)
