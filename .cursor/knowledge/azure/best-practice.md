# Azure Knowledge Base - Best Practices

## Tổng quan

Document này cung cấp 10+ best practices cho việc sử dụng Azure trong Cursor Enterprise Framework, kèm theo code examples cụ thể cho từng practice.

## Practice 1: Use Resource Groups Effectively

### Mô tả

Tổ chức resources trong resource groups một cách có ý nghĩa để simplify management, billing, và access control.

```bash
# Create resource groups for different environments
az group create --name myapp-prod-rg --location eastus
az group create --name myapp-staging-rg --location eastus
az group create --name myapp-dev-rg --location westus2

# Tag resource groups
az group update --name myapp-prod-rg \
  --set tags.Environment=Production tags.Team=Platform tags.CostCenter=CC-1234
```

```bash
# List resources with tags
az resource list --tag Environment=Production --output table
```

### Tại sao quan trọng

- **Organization**: Resources dễ tìm và manage
- **Billing**: Track costs by resource group
- **Access Control**: Apply RBAC at resource group level
- **Lifecycle**: Delete entire resource groups to clean up

## Practice 2: Use Managed Identities

### Mô tả

Managed identities eliminates need to manage credentials. Azure automatically handles credential rotation.

```bash
# Enable system-assigned managed identity on a VM
az vm identity assign \
  --resource-group myResourceGroup \
  --name myVM

# Get the principal ID
az vm identity show \
  --resource-group myResourceGroup \
  --name myVM \
  --query principalId
```

```typescript
// Use managed identity in code (TypeScript)
import { DefaultAzureCredential } from "@azure/identity";

async function main() {
  const credential = new DefaultAzureCredential();
  
  // Azure SDK automatically uses managed identity
  const { token } = await credential.getToken(
    "https://storage.azure.com/.default"
  );
  
  // Use token for Azure Storage operations
  const response = await fetch(
    "https://mystorageaccount.blob.core.windows.net/mycontainer/myblob",
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );
  
  return response.json();
}
```

```yaml
# ARM template with managed identity
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/...",
  "resources": [
    {
      "type": "Microsoft.Web/sites",
      "apiVersion": "2022-03-01",
      "identity": {
        "type": "SystemAssigned"
      },
      "properties": {
        "siteConfig": {
          "appSettings": [
            {
              "name": "AZURE_CLIENT_ID",
              "value": "[reference(resourceId('Microsoft.Web/sites', variables('webAppName')), '2022-03-01', 'full').identity.principalId]"
            }
          ]
        }
      }
    }
  ]
}
```

## Practice 3: Implement Network Security

### Mô tả

Sử dụng network security groups (NSGs) và service endpoints để secure network traffic.

```bash
# Create NSG
az network nsg create \
  --resource-group myResourceGroup \
  --name myNSG

# Add security rules
az network nsg rule create \
  --resource-group myResourceGroup \
  --nsg-name myNSG \
  --name AllowHTTPS \
  --priority 100 \
  --source-address-prefixes Internet \
  --destination-address-prefixes VirtualNetwork \
  --destination-port-ranges 443 \
  --access Allow \
  --protocol Tcp

az network nsg rule create \
  --resource-group myResourceGroup \
  --nsg-name myNSG \
  --name DenyAllInbound \
  --priority 4096 \
  --source-address-prefixes Internet \
  --destination-address-prefixes VirtualNetwork \
  --destination-port-ranges "*" \
  --access Deny \
  --protocol "*"

# Associate NSG with subnet
az network vnet subnet update \
  --resource-group myResourceGroup \
  --vnet-name myVNet \
  --name mySubnet \
  --network-security-group myNSG
```

```bash
# Enable service endpoints for storage
az network vnet subnet update \
  --resource-group myResourceGroup \
  --vnet-name myVNet \
  --name mySubnet \
  --service-endpoints Microsoft.Storage Microsoft.KeyVault
```

## Practice 4: Use Azure Key Vault for Secrets

### Mô tả

Store all secrets, keys, và certificates trong Azure Key Vault thay vì in code hoặc config files.

```bash
# Create Key Vault
az keyvault create \
  --resource-group myResourceGroup \
  --name myKeyVault \
  --sku Premium \
  --enable-rbac-authorization true

# Set secrets
az keyvault secret set \
  --vault-name myKeyVault \
  --name "DbPassword" \
  --value "supersecretpassword"

az keyvault secret set \
  --vault-name myKeyVault \
  --name "ApiKey" \
  --value "apikeyvalue"

# Create certificate
az keyvault certificate create \
  --vault-name myKeyVault \
  --name myCertificate \
  --policy "$(az keyvault certificate get-default-policy)"

# Grant access to Key Vault
az role assignment create \
  --assignee <user-or-app-id> \
  --role "Key Vault Secrets User" \
  --scope "/subscriptions/{subscription-id}/resourceGroups/{rg-name}/providers/Microsoft.KeyVault/vaults/{vault-name}"
```

```typescript
// Access Key Vault secrets in code
import { SecretClient } from "@azure/keyvault-secrets";
import { DefaultAzureCredential } from "@azure/identity";

async function getSecret(secretName: string): Promise<string> {
  const credential = new DefaultAzureCredential();
  
  const client = new SecretClient(
    "https://myKeyVault.vault.azure.net/",
    credential
  );
  
  const secret = await client.getSecret(secretName);
  return secret.value!;
}

// Use in configuration
const dbPassword = await getSecret("DbPassword");
```

## Practice 5: Implement Backup và Disaster Recovery

### Mô tả

Configure backup và geo-redundancy để ensure business continuity.

```bash
# Enable Azure Backup for VM
az backup protection enable-for-vm \
  --resource-group myResourceGroup \
  --vault-name myRecoveryServicesVault \
  --vm myVM \
  --policy-name DefaultPolicy

# Create geo-redundant storage
az storage account create \
  --resource-group myResourceGroup \
  --name mystorageaccount \
  --sku Standard_GRS

# Configure Azure SQL geo-replication
az sql db replica create \
  --resource-group myResourceGroup \
  --server myserver \
  --name myDatabase \
  --partner-resource-group partnerRG \
  --partner-server partnerServer \
  --elastic-pool-name myElasticPool
```

```bash
# Enable Azure Site Recovery for VMs
az extension add --name site-recovery
az backup vault create \
  --resource-group myResourceGroup \
  --name myRecoveryVault

# Configure replication
az site-recovery service configure-replication \
  --resource-group myResourceGroup \
  --vault-name myRecoveryVault \
  --fabric Azure \
  --vm-protection-target vm-id
```

## Practice 6: Use Azure Policy for Governance

### Mô tả

Implement Azure Policy để enforce organizational standards và compliance.

```json
{
  "properties": {
    "displayName": "Require HTTPS for Storage Accounts",
    "description": "This policy ensures all storage accounts require HTTPS.",
    "mode": "Indexed",
    "parameters": {
      "effect": {
        "type": "String",
        "defaultValue": "Deny",
        "allowedValues": ["Deny", "Audit", "Disabled"]
      }
    },
    "policyRule": {
      "if": {
        "allOf": [
          {
            "field": "type",
            "equals": "Microsoft.Storage/storageAccounts"
          },
          {
            "not": {
              "field": "Microsoft.Storage/storageAccounts/supportsHttpsTrafficOnly",
              "equals": "true"
            }
          }
        ]
      },
      "then": {
        "effect": "[parameters('effect')]"
      }
    }
  }
}
```

```bash
# Create policy definition
az policy definition create \
  --name "require-https-storage" \
  --display-name "Require HTTPS for Storage Accounts" \
  --description "This policy ensures all storage accounts require HTTPS." \
  --mode Indexed \
  --rules policy.json

# Assign policy to resource group
az policy assignment create \
  --name "require-https-storage-assignment" \
  --scope "/subscriptions/{subscription-id}/resourceGroups/myResourceGroup" \
  --policy "require-https-storage"
```

## Practice 7: Implement Autoscaling

### Mô tả

Configure autoscaling để handle variable workloads efficiently.

```bash
# Create autoscale settings for App Service
az monitor autoscale create \
  --resource-group myResourceGroup \
  --resource myAppServicePlan \
  --resource-type Microsoft.Web/serverfarms \
  --name myAutoscaleSettings

# Add scaling rules
az monitor autoscale rule create \
  --resource-group myResourceGroup \
  --autoscale-name myAutoscaleSettings \
  --condition "Percentage CPU > 70" \
  --timeAggregation Average \
  --conditionTime 5 \
  --scaleDirection Increase \
  --scaleType ChangeCount \
  --scaleValue 1

az monitor autoscale rule create \
  --resource-group myResourceGroup \
  --autoscale-name myAutoscaleSettings \
  --condition "Percentage CPU < 30" \
  --timeAggregation Average \
  --conditionTime 5 \
  --scaleDirection Decrease \
  --scaleType ChangeCount \
  --scaleValue 1

# Set scale limits
az monitor autoscale settings set \
  --resource-group myResourceGroup \
  --name myAutoscaleSettings \
  --min-count 2 \
  --max-count 10
```

```yaml
# AKS autoscaling (Kubernetes)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## Practice 8: Use Azure Monitor Effectively

### Mô tả

Implement comprehensive monitoring để track performance, availability, và security.

```bash
# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --resource-group myResourceGroup \
  --workspace-name myWorkspace

# Enable Azure Monitor for VMs
az monitor diagnostic-settings create \
  --resource myVM \
  --workspace myWorkspace \
  --logs '[
    {
      "category": "ApplicationEvent",
      "enabled": true
    }
  ]' \
  --metrics '[
    {
      "category": "AllMetrics",
      "enabled": true
    }
  ]'
```

```bash
# Create alert rules
az monitor alert create \
  --resource-group myResourceGroup \
  --name cpu-alert \
  --target myVM \
  --condition "Percentage CPU > 80" \
  --time-aggregation-type Average \
  --window-size 5m \
  --severity Warning \
  --description "CPU usage is high"
```

```typescript
// Application Insights integration
import { ApplicationInsights } from "@microsoft/applicationinsights-web";

const appInsights = new ApplicationInsights({
  config: {
    connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING,
    enableAutoRouteTracking: true
  }
});

appInsights.loadAppInsights();

// Track custom events
appInsights.trackEvent({
  name: "UserLoggedIn",
  properties: {
    userId: user.id,
    timestamp: new Date().toISOString()
  }
});

// Track exceptions
try {
  await riskyOperation();
} catch (error) {
  appInsights.trackException({ error });
}
```

## Practice 9: Implement Cost Management

### Mô tả

Monitor và optimize costs sử dụng Azure Cost Management.

```bash
# Create budget alert
az costmanagement budget create \
  --resource-group myResourceGroup \
  --name myBudget \
  --amount 1000 \
  --time-grain Monthly \
  --start-date 2024-01-01 \
  --category Cost \
  --notification-operator GreaterThan \
  --notification-threshold 90

# Set cost alerts
az costmanagement alert create \
  --resource-group myResourceGroup \
  --name myAlert \
  --scope /subscriptions/{subscription-id} \
  --type Budget \
  --threshold 1000
```

```bash
# Export cost data
az costmanagement export create \
  --name myExport \
  --resource-group myResourceGroup \
  --storage-account mystorageaccount \
  --storage-container-name exports \
  --start-date 2024-01-01 \
  --timeframe MonthToDate \
  --type ActualCost
```

## Practice 10: Use Bicep/ARM for Infrastructure as Code

### Mô tả

Define infrastructure as code để enable version control, review, và automated deployment.

```bicep
// main.bicep
param location string = resourceGroup().location
param webAppName string = 'myWebApp-${uniqueString(resourceGroup().id)}'
param sku string = 'B1'
param linuxFxVersion string = 'DOTNET|6.0'

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: '${webAppName}-asp'
  location: location
  sku: {
    name: sku
  }
}

// Web App
resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: webAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: linuxFxVersion
      appSettings: [
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
      ]
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}

// Output
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output webAppName string = webApp.name
```

```bash
# Deploy with Azure CLI
az deployment group create \
  --resource-group myResourceGroup \
  --template-file main.bicep \
  --parameters webAppName=myApp sku=B1
```

## Practice 11: Implement RBAC Properly

### Mô tả

Use role-based access control để grant least privilege access.

```bash
# Create custom role
az role definition create \
  --role-definition '{
    "Name": "App Reader",
    "Description": "Read access for application resources",
    "actions": [
      "Microsoft.Web/sites/read",
      "Microsoft.Web/serverfarms/read",
      "Microsoft.Storage/storageAccounts/read",
      "Microsoft.Insights/components/read"
    ],
    "notActions": [],
    "dataActions": [],
    "notDataActions": []
  }'

# Assign role to user
az role assignment create \
  --assignee user@example.com \
  --role "App Reader" \
  --resource-group myResourceGroup

# Assign role to managed identity
az role assignment create \
  --assignee $(az webapp show --name myApp --query identity.principalId --output tsv) \
  --role "Storage Blob Data Reader" \
  --scope /subscriptions/{subscription-id}/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/mystorageaccount
```

## Practice 12: Use Azure Advisor

### Mô tả

Review Azure Advisor recommendations để optimize deployments.

```bash
# List recommendations
az advisor recommendation list \
  --resource-group myResourceGroup \
  --category Security

# Get specific recommendation
az advisor recommendation show \
  --resource /subscriptions/{subscription-id}/resourceGroups/myResourceGroup/providers/Microsoft.Compute/virtualMachines/myVM \
  --recommendation-id ab3e-xxx

# Suppress recommendation
az advisor recommendation update \
  --ids /subscriptions/{subscription-id}/providers/Microsoft.Advisor/recommendations/ab3e-xxx \
  --suppression-name mySuppression \
  --suppression-length 30
```

## Related Documents

- [Azure Glossary](../glossary.md)
- [Azure Architecture](../architecture.md)
- [Azure Anti-Patterns](../anti-pattern.md)
- [Azure Checklist](../checklist.md)
- [Azure FAQ](../faq.md)
- [Azure Decision Tree](../decision-tree.md)
