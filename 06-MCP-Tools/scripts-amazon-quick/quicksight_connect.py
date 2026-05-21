import boto3
from botocore.exceptions import ClientError, NoCredentialsError

ACCOUNT_ID = "588957334073"
REGION = "us-west-2"  # QuickSight está nesta região

qs = boto3.client("quicksight", region_name=REGION)

def listar_dashboards():
    resp = qs.list_dashboards(AwsAccountId=ACCOUNT_ID)
    items = resp.get("DashboardSummaryList", [])
    print(f"\n📊 Dashboards ({len(items)}):")
    for d in items:
        print(f"  - {d['Name']} | ID: {d['DashboardId']}")

def listar_datasets():
    resp = qs.list_data_sets(AwsAccountId=ACCOUNT_ID)
    items = resp.get("DataSetSummaries", [])
    print(f"\n🗄️ Datasets ({len(items)}):")
    for d in items:
        print(f"  - {d['Name']} | ID: {d['DataSetId']}")

def listar_usuarios():
    resp = qs.list_users(AwsAccountId=ACCOUNT_ID, Namespace="default")
    items = resp.get("UserList", [])
    print(f"\n👥 Usuários ({len(items)}):")
    for u in items:
        print(f"  - {u['UserName']} | Role: {u['Role']} | Email: {u['Email']}")

if __name__ == "__main__":
    print("🔌 Conectando ao QuickSight...")
    try:
        listar_usuarios()
        listar_dashboards()
        listar_datasets()
        print("\n✅ Conexão OK!")
    except ClientError as e:
        print(f"\n❌ Erro: {e.response['Error']['Message']}")
