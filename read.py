import os

import setting
import helper


#   Get the Last User ID number
#   Input format:   None
#   Return format:  int
def get_previous_user_id():
    UserAccList = open(setting.UserAccPath, "r")
    printout = ""
    for data in UserAccList:
        for x in range(len(data) - 1):
            printout = ""
            printout = printout + data[x]
    UserAccList.close()
    if printout[0] < "1" or printout[0] > "9":
        return 1
    else:
        number = ""
        if printout[1] == " ":
            number = printout[0]
        elif printout[2] == " ":
            number = printout[0:2]
        elif printout[3] == " ":
            number = printout[0:3]
        elif printout[4] == " ":
            number = printout[0:4]
        elif printout[5] == " ":
            number = printout[0:5]
        return int(number) + 1


#   Print All the User Information
#   Input format:   None
#   Return format:  None
def print_user_info():
    UserAccList = open(setting.UserAccPath, "r")
    for data in UserAccList:
        printout = data[:-1]
        print(printout)
    UserAccList.close()
    print("")


#   Check if the username exist already
#   Input format:   str
#   Return format:  boolean
def check_if_username_used(input_username):
    exist = False
    data_username = ""
    UserAccList = open(setting.UserAccPath, "r")
    for data in UserAccList:
        data_username = data[8:24]
        actual_username = helper.delete_empty_space(data_username)
        if actual_username == input_username:
            exist = True
            break
    UserAccList.close()
    return exist


#   Add Account into Account List
#   Input format:   str,str
#   Return format:  boolean
def add_account(username, password):
    if not check_if_username_used(username):
        #   Get Previous User ID
        next_user_id = get_previous_user_id()
        UserAccList = open(setting.UserAccPath, "a")
        UserInfoList = open(setting.UserInfoPath, "a")
        gap_user_ID = 8 - len(str(next_user_id))
        gap_user_ID_string = ""
        gap_username = 16 - len(username)
        gap_username_string = ""
        for x in range(gap_user_ID):
            gapUserIDStr = gapUserIDStr + " "
        for y in range(gap_username):
            gapUsernameStr = gapUsernameStr + " "
        UserAccList.write(
            str(next_user_id)
            + gap_user_ID_string
            + username
            + gap_username_string
            + password
            + "\n"
        )
        UserAccList.close()

        UserInfoList.write(
            str(next_user_id)
            + gap_user_ID_string
            + username
            + gap_username_string
            + str(3)
            + "       "
            + str(0)
            + "\n"
        )
        UserInfoList.close()

        helper.display_heading("Account Successfully Registered", 1)
        print("")
        return True
    else:
        helper.display_heading("Your username is being used already", 1)
        return False


#   Check if the password correct
#   Input format:   str,str
#   Return format:  boolean
def check_if_login_correct(input_username, input_password):
    correct = False
    data_username = ""
    data_password = ""
    UserAccList = open(setting.UserAccPath, "r")
    for data in UserAccList:
        data_username = data[8:24]
        actual_username = helper.delete_empty_space(data_username)
        if actual_username == input_username:
            data_password = data[24:-1]
            actual_password = helper.delete_empty_space(data_password)
            if actual_password == input_password:
                correct = True
                break
    UserAccList.close()
    return correct


#   Update the Score of the user if logged in
#   Input format:   str,int,int
#   Return format:  None
def update_score_by_id(id, score, played_game):
    total_data = []
    #   Read the Info
    UserInfoListRead = open(setting.UserInfoPath, "r+")
    for read_data in UserInfoListRead:
        total_data.append(read_data[:-1])
    UserInfoListRead.close()

    #   Edit the score
    target_string = total_data[id]
    score_empty = 8 - len(str(score))
    score_string = ""
    for x in range(score_empty):
        score_string = score_string + " "
    update_string = target_string[:24] + str(score) + score_string + str(played_game)
    total_data[id] = update_string

    #   Write the Info
    UserInfoList = open(setting.UserInfoPath, "w+")
    for x in range(len(total_data)):
        UserInfoList.write(total_data[x])
        UserInfoList.write("\n")
    UserInfoList.close()

    #   Update the Score of the user if logged in


#   Input format:   str,int,int
#   Return format:  None
def update_score_by_name(username, score, played_game):
    id = get_user_id_by_username(username)
    update_score_by_id(id, score, played_game)


def get_user_id_by_username(username):
    UserAccList = open(setting.UserAccPath, "r")
    for data in UserAccList:
        data_username = data[8:24]
        actual_username = helper.delete_empty_space(data_username)
        if actual_username == username:
            number = ""
            if data[1] == " ":
                number = data[0]
            elif data[2] == " ":
                number = data[0:2]
            elif data[3] == " ":
                number = data[0:3]
            elif data[4] == " ":
                number = data[0:4]
            elif data[5] == " ":
                number = data[0:5]
            return int(number)
    UserAccList.close()
    return -1


def get_score_by_username(username):
    data_username = ""
    UserInfoList = open(setting.UserInfoPath, "r")
    for data in UserInfoList:
        data_username = data[8:24]
        actual_username = helper.delete_empty_space(data_username)
        if actual_username == username:
            score = data[24:32]
            actual_score = helper.delete_empty_space(score)
            return int(actual_score)
    UserInfoList.close()
    return -1


def get_played_game_by_username(username):
    data_username = ""
    UserInfoList = open(setting.UserInfoPath, "r")
    for data in UserInfoList:
        data_username = data[8:24]
        actual_username = helper.delete_empty_space(data_username)
        if actual_username == username:
            played_game = data[32:-1]
            actual_played_game = helper.delete_empty_space(played_game)
            return int(actual_played_game)
    UserInfoList.close()
    return -1
