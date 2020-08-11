import pymongo

client = pymongo.MongoClient(
        "mongodb+srv://admin:admin@walllet-oykbx.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]
users_col = db["users"]
user = {}
users = []

for index in range(30000):
    user["firstName"] = ""
    user["lastName"] = ""
    user["email"] = ""
    user["password"] = ""
    user["answerPassword"] = ""
    user["phoneNumber"] = ""
    user["yearOfBirth"] = ""
    user["maritalStatus"] = ""
    user["addictedStatus"] = ""
    user["myTarget"] = ""
    user["walletMember"] = ""
    user["friendMember"] = ""
    user["myWalletMembers"] = ""
    user["myFixedExpenses"] = ""
    user["myFixedIncomes"] = ""
    user["passes"] = ""
    users.append(user)
    
users_col.insert_many(users)
