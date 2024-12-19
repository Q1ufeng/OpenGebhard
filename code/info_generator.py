import random
import string
import math


def generate_random_strings(length, min_len, max_len):
    generated_strings = set()

    while len(generated_strings) < length:
        str_len = random.randint(min_len, max_len)
        random_string = ''.join(random.choices(string.ascii_lowercase, k=str_len))
        generated_strings.add(random_string)

    return list(generated_strings)


def info_generator(people_num_sqrt, book_num):

    people_names = []
    people_addr = []
    people_depo = []
    book_names = []
    book_stock = []
    book_price = []
    
    firstnames = generate_random_strings(people_num_sqrt, 3, 10)
    lastnames = generate_random_strings(people_num_sqrt, 3, 10)
    for x in firstnames:
        for y in lastnames:
            people_names.append(x + "-" + y)
            
    people_addr = generate_random_strings(people_num_sqrt*people_num_sqrt,10,30)
    
    for i in range(people_num_sqrt*people_num_sqrt):
        people_depo.append(random.randint(50,200))    
        
    book_names = generate_random_strings(book_num, 3, 30)
    
    for i in range(book_num):
        book_stock.append(random.randint(1,200))
        book_price.append(random.randint(20,40))

    return people_names,people_addr,people_depo,book_names,book_stock,book_price
