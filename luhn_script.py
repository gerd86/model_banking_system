import random


# TODO: Split function into functions that deal with seperate concerns
# TODO: A credit card generator function
# TODO: Luhn Algortihm CheckSum Generator
# TODO: Luhn ALgorithm Checker

def credit_card_generator():
    bank_id = 400000
    acc_id = random.randrange(10 ** 8, 10 ** 9)
    credit_card_number = f'{bank_id}{acc_id}'
    split_list = list(map(int, credit_card_number))
    # Multiply odd digits by 2
    new_list = [x * 2 if i % 2 else x for i, x in enumerate(split_list)]
    print(new_list)
    # Subtract 9 from numbers over 9
    subtract_list = [x - 9 if x > 9 else x for x in new_list]
    # What number is the checksum?
    remainder = 10 - (sum(subtract_list) % 10)
    # Add final number to credit card number
    final_number = f'{credit_card_number}{remainder}'
    return final_number



# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
def luhn_checksum(crd_num):
    int_list = list(map(int, crd_num))
    last_digit = int_list.pop()
    multiple_list = [x * 2 if i % 2 else x for i, x in enumerate(int_list)]
    minus_nine = [x - 9 if x > 9 else x for x in multiple_list]
    sum_plus_last = sum(minus_nine) + last_digit
    if sum_plus_last % 10 == 0:
        print("Number is correct")
    else:
        print("Invalid number")


num = credit_card_generator()
luhn_checksum(num)