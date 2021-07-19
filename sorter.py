import os
from operator import index, itemgetter
from sys import prefix
from typing_extensions import final
from robot.api.deco import keyword

BLANK_SPACES = '    '
BLANK_SPACE = ' '
PROJECT_PATH = os.getcwd() + '\\..\\..\\..\\'


def get_files(root_path: str = PROJECT_PATH):
    list_of_files = []
    for (dir_path, dir_names, filenames) in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.robot'):
                if not str(dir_path).endswith('\\'):
                    dir_path += '\\'
                list_of_files.append(dir_path + filename)

    return list_of_files

def open_file(file_path: str) -> list:
    file = open(file_path, encoding='UTF-8')
    file_content = file.readlines()
    file.close()
    file_list = []
    for line in file_content:
        new_line = line.replace('\n', '').replace('\r', '')
        if new_line is not '':
            file_list.append(line.replace('\n', '').replace('\r', ''))

    return file_list

def slice_file(file: list, begin_marker: str, end_marker: str = None):

    # Find first index. Using loop and contains because not always we 
    # can match the word style for using a .index method

    first_index = 0
    for f in file:
        first_index += 1
        if f.__contains__(begin_marker):
            break

    last_index = 0
    if end_marker:
        for f in file:
            last_index += 1
            if f.__contains__(end_marker):
                break
    else:
        last_index = len(file)

    return file[first_index:last_index]


def get_keywords(file: list):

    keywords_list = []
    for line in file:    
        if not line.startswith(BLANK_SPACES):
            keywords_content = []
            keywords_list.append([line,keywords_content])
        else:
            keywords_content.append(line)

    return keywords_list

# Get the comments plus one line bellow, to know from where is that comment
def get_comments(file: list):
    comments_list = []
    comments = []
    flag = False
    contains_comments = False
    for line in file:
        if line.startswith("#"):
            comments.append(line)
            flag = True
            contains_comments = True
        else:
            if flag and not line.startswith(BLANK_SPACES):
                comments.append(line)
                comments_list.append(comments)
                comments = []
                flag = False
                continue

    if contains_comments:
        return comments_list
    else:
        return False



def put_comments(file: list, comments: list):
    for line in file:
        for comment in comments:
            if line == comment[-1]:
                print(comment)


def get_header(file: list):
    index = 0
    for f in file:
        index += 1
        if f.__contains__('Test Cases'):
            break

    return file[:index]

def sort_keywords(_keywords_list: list) -> list:
    sorted_list = sorted(_keywords_list, key=itemgetter(0))

    # Create list of the sorted scenarios
    final_list = []
    for i in range(len(sorted_list)):
        final_list.append('\n')
        final_list.append(sorted_list[i][0])
        for w in sorted_list[i][1]:
            final_list.append(w)

    return final_list

def output_file(keywords: list, key: str):

    if key == 'Keywords':
        print('*** Keywords ***')
    if key == 'Test Cases':
        print('*** Test Cases ***')
    for k in keywords:
        print(k)


if __name__ == '__main__':
    path = 'C:\\Users\\victor.ferreira\\Documents\\workspace\\will-qa-mobile\\temp\\'
    file_name = 'test_cases.robot'

    file = open_file(path + file_name)
    comments = get_comments(file)


    # put_comments(file, comments)

    # Separate hearder file
    hearder_file = get_header(file)
    for h in hearder_file:
        print(h)
        if h.__contains__('Settings'):
            print()
        if h.__contains__('Test Cases'):
            hearder_file.remove(h)

    # Sort Test Cases
    key = 'Test Cases'
    file_chunck = slice_file(file, key)
    keywords = get_keywords(file_chunck)
    keywords_sorted = sort_keywords(keywords)
    
    output_file(keywords_sorted, key)



    # Sort Keywords
    # key = 'Keywords'
    # file_chunck = slice_file(file, key)
    # keywords = get_keywords(file_chunck)
    # keywords_sorted = sort_keywords(keywords)
    # output_file(keywords_sorted, key)
