# Tiqets Assignment

## Contents

1. [Description](#description)
2. [Run](#run)
3. [Output](#output)
4. [SQL Data Model](#sql-data-model)

## Description
A program that reads 2 datasets, orders.csv and barcodes.csv, and generates an
output csv file with all the barcodes and orders_ids per customer.

Duplicated barcodes are ignored as well as orders without barcodes.
They can be found in stdout or [output.log](./output.log)

Additionally, it calculates top 5 customers that bought the most amount of tickets and the amount of unused barcodes.

## Run
### Pre-requirements
* [Docker](https://www.docker.com/) installed

### Commands
1. `docker build -t tiqets .`
2. `docker run --rm -it -v ${PWD}:/app tiqets`

## Output
Result file can be found [here](./result.csv).

Logs are printed out in stdout and tracked in the [output.log](./output.log) file.

## SQL Data Model
* Table Customers

| Column Name                         | Type | Constraint  |
|-------------------------------------|------|-------------|
| customer_id                         | int  | primary key |
| other relevant customer information | ...  |             |

* Table Orders

| Column Name                       | Type | Constraint  |
|-----------------------------------|------|-------------|
| order_id                          | int  | primary key |
| barcode                           | int  | foreign key |
| other relevant orders information | ...  |             |

* Table Orders_Customers

| Column Name | Type | Constraint  |
|-------------|------|-------------|
| order_id    | int  | foreign key |
| customer_id | int  | foreign key |

* Products

| Column Name                                                                   | Type | Constraint  |
|-------------------------------------------------------------------------------|------|-------------|
| barcode                                                                       | int  | primary key |
| other relevant information about the product (product name, description etc.) | ...  |             |