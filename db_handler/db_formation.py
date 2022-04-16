import csv
import pandas as pd


def csv_save_user(user_id, user_input):
    """
    save user inputs in db
    """
    with open(".//db_handler//user_inputs.csv", "a", encoding='UTF-8') as db:
        writer = csv.writer(db, delimiter="\t", lineterminator="\n")

        if open(".//db_handler//user_inputs.csv", "r").read() == "":
            writer.writerow(["user_id", "user_input"])
        
        writer.writerow([user_id, user_input]) 


def user_pass(user_id, attempts_number, right_password) -> tuple:
    """
    Check user input. Return ({True in case of correct input 
    else False}, {number of attempts})
    """
    df_users = pd.read_csv(".//db_handler//user_inputs.csv", sep='\t')
    
    # procede db
    users_inputs = list(df_users[df_users['user_id']==user_id]["user_input"])
    count_tries = df_users[df_users['user_id']==user_id]["user_input"].count()


    if count_tries < attempts_number and right_password in users_inputs:
        df_users = df_users[df_users['user_id'] != user_id]
        df_users.to_csv(".//db_handler//user_inputs.csv", sep='\t', index=False)
        df_users = pd.read_csv(".//db_handler//user_inputs.csv", sep='\t')
        return (True, count_tries)
    
    elif count_tries < attempts_number and right_password not in users_inputs:
        return (False, count_tries)
    
    elif count_tries >= attempts_number:
        return (False, count_tries)