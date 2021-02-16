# ========================================================================
# Copyright 2021 Emory University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================
##THIS CODE WAS MY OWN WORK,
##IT WAS WRITTEN WITHOUT CONSULTING ANYSOURCES
##OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR.
##Wali Khan 2308097
import re


def normalize(text):
    # TODO: to be updated
    text = text.replace('-', ' ')
    text = text.replace(r'\W', '')
    result = []
    newtext = text.lower()
    numbers1 = [['zero', '0'], ['one', '1'], ['two', '2'], ['three', '3'], ['four', '4'], ['five', '5'], ['six', '6'],
                ['seven', '7'],
                ['eight', '8'], ['nine', '9'], ['ten', '10']]
    numbers2 = [['twenty', '20'], ['thirty', '30'], ['fourty', '40'], ['fifty', '50'], ['sixty', '60'],
                ['seventy', '70'], ['eighty', '80'], ['ninety', '90']]
    numbers3 = [['hundred', '100'], ['thousand', '1000'], ['million', '1000000'], ['billion', '1000000000']]
    teens = [['eleven', '11'], ['twelve', '12'], ['thirteen', '13'], ['fourteen', '14'], ['fifteen', '15'],
             ['sixteen', '16'], ['seventeen', '17'], ['eighteen', '18'], ['nineteen', '19']]
    one_ten = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    ten_nine = ['10', '20', '30', '40', '50', '60', '70', '80', '90']
    big = ['1000', '1000000', '1000000000']
    words = text.split()
    test = newtext.split()
    i = 0
    while (i < len(words)):
        walk = next((entry for entry in numbers1 if test[i] == entry[0]), None)
        walk2 = next((entry2 for entry2 in numbers2 if test[i] == entry2[0]), None)
        walk3 = next((entry3 for entry3 in numbers3 if test[i] == entry3[0]), None)
        walk4 = next((entry4 for entry4 in teens if test[i] == entry4[0]), None)
        if walk:
            number = walk[1]
            result.append(number)
            i += 1
        elif walk2:
            number2 = walk2[1]
            result.append(number2)
            i += 1
        elif walk3:
            number3 = walk3[1]
            result.append(number3)
            i += 1
        elif walk4:
            number4 = walk4[1]
            result.append(number4)
            i += 1
        else:
            result.append(words[i])
            i += 1

    k = 0
    result2 = []
    while (k < len(result)):
        pointer = result[k]
        verify1 = next((t for t in numbers1 if result[k] == t[1]), None)
        verify2 = next((t for t in teens if result[k] == t[1]), None)
        verify3 = next((t for t in numbers2 if result[k] == t[1]), None)
        verify4 = next((t for t in numbers3 if result[k] == t[1]), None)

        if verify4:
            if result[k] == '1000000':
                if not result[k + 1].isnumeric():
                    result2.append('000000')

                elif '1000' not in result:
                    result2.append('000')



            elif result[k] == '1000':
                if not result[k + 1].isnumeric():
                    result2.append('000')





            elif result[k] == '1000000000':
                if not result[k + 1].isnumeric():
                    result2.append('000000000')

                elif '1000000' not in result:
                    result2.append('000')



            elif result[k] == '100':
                if not result[k + 1].isnumeric():
                    result2.append('00')

            k += 1
        elif verify3:
            addthis = str(verify3[1])
            if result[k - 1] in big and result[k + 1] in one_ten:
                addthis = '0' + addthis[0]
                result2.append(addthis)
                k += 1
            elif result[k - 1] in big and result[k + 1] not in one_ten:
                addthis = '0' + addthis
                result2.append(addthis)
                k += 1
            elif result[k + 1] in one_ten:
                result2.append(addthis[0])
                k += 1
            else:
                result2.append(addthis)
                k += 1

        elif verify2:
            addthis = verify2[1]
            result2.append(addthis)
            k += 1

        elif verify1:
            addthis = verify1[1]
            if result[k - 1] in big and result[k + 1] != '100':
                addthis = '00' + addthis
                result2.append(addthis)
                k += 1

            else:
                result2.append(addthis)
                k += 1

        elif result[k] == 'a' and result[k + 1] in big:
            result2.append('1')
            k += 1
        else:
            result2.append(result[k])
            k += 1

    j = 0
    answer = ''
    while (j < len(result2) - 1):
        if not result2[j].isnumeric():
            answer += result2[j] + ' '
            j += 1
        elif result2[j].isnumeric() and not result2[j + 1].isnumeric():
            answer += result2[j] + ' '
            j += 1
        else:
            answer += result2[j]
            j += 1

    answer += result2[j]

    return answer


# def normalize_extra(text):
#     # TODO: to be updated
#     return text


if __name__ == '__main__':
    S = [
        'I met twelve people',
        'I have one brother and two sisters',
        'A year has three hundred sixty five days',
        'I made a million dollars'
    ]

    T = [
        'I met 12 people',
        'I have 1 brother and 2 sisters',
        'A year has 365 days',
        'I made 1000000 dollars'
    ]

    correct = 0
    for s, t in zip(S, T):
        if normalize(s) == t:
            correct += 1

    print('Score: {}/{}'.format(correct, len(S)))





