import os

puri = os.environ.get('DATABASE_URL','postgres://seqmujfcvmcqhh:91bad46d3e7e5df3ff53d48a41e27fd9ac827acae2b75d2eb12b9722f939e860@ec2-18-206-20-102.compute-1.amazonaws.com:5432/d5gkt64aa114el')
filler, credentials = puri.split("postgres://")
slice1, slice2 = credentials.split("@")
username, password = slice1.split(":")
host, slice3 = slice2.split(":")
port, database = slice3.split("/")

aiem_config = {
    'dbname': database,
    'user': username,
    'host': host,
    'password': password,
    'port': port
}
