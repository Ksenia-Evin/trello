import sys
import requests  
  
# Данные авторизации в API Trello  
auth_params = {    
    'key': "d31b612b888c1aa6ff556dd0f72e1ccc",    
    'token': "e3af6a6e422bdd9f662a3fd6dd964391b0aa7dcb9e75124f13978b4a991c8b59", 
}  
  
# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}"  

board_id = "GLbHmh1L"

def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()   
        print(column['name'] + '\t' +'Задач в списке: {}'.format(len(task_data)))       
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'] + '\t' + 'id задачи: {}'.format(task['id']))  

def tasksDublicates(task_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    dublicates = []
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()   
        for task in task_data:
            if task['name'] == task_name:
                dublicates.append(task)
    return dublicates

def create(name, column_name): 
    column_id = column_exist(column_name)
    if column_id is None:
        column_id = createColumn(column_name)['id'] 
    requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth_params})      

        

def column_exist(column_name):
    column_id = None
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == column_name:
            column_id = column['id']
            return column_id


def createColumn(column_name):
    response = requests.get(base_url.format('boards/' + board_id), params=auth_params).json()
    board_id_new = response['id']
    requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': board_id_new, **auth_params})

def move(name, column_name):
    dublicates = tasksDublicates(name)
    if len(dublicates) > 1:
        print('Несколько задач с таким именем!')
        for index, task in enumerate(dublicates):  
            task_column_name = requests.get(base_url.format('lists') + '/' + task['idList'], params=auth_params).json()['name']  
            print("Задача №{}\tid: {}\tНаходится в колонке: {}\t ".format(index, task['id'], task_column_name))  
        task_id = input("Пожалуйста, введите ID задачи, которую нужно переместить: ")  
    else:  
        task_id = dublicates[0]['id']

    column_id = column_exist(column_name)
    if column_id is None:
        column_id = createColumn(column_name)['id']
    requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column_id, **auth_params})


if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3]) 
    elif sys.argv[1] == 'col':
        createColumn(sys.argv[2])  