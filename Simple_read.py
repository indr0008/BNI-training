# Import necessary Spark modules
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, count, col

# Create a Spark session
spark = SparkSession.builder.appName("BankingTransactionAnalysis").getOrCreate()

# Load the banking transaction data into a Spark DataFrame
transaction_data = spark.read.csv("path/to/your/transaction_data.csv", header=True, inferSchema=True)

# Show the schema of the DataFrame
transaction_data.printSchema()

# Perform some basic analysis
total_transactions = transaction_data.count()
total_deposit_amount = transaction_data.filter(col("transaction_type") == "deposit").agg(sum("amount")).first()[0]
total_withdrawal_amount = transaction_data.filter(col("transaction_type") == "withdrawal").agg(sum("amount")).first()[0]

# Show the results
print(f"Total Transactions: {total_transactions}")
print(f"Total Deposit Amount: {total_deposit_amount}")
print(f"Total Withdrawal Amount: {total_withdrawal_amount}")

# Stop the Spark session
spark.stop()
