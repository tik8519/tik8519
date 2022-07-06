def encrypt(message):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'( ./"
    message = message.split(' ')
    new_message = []
    for word in message:
        new_word = ''
        for i in word:
            for x in range(len(letters)):
                if i == letters[x]:
                    new_word += letters[x-1]
            if i == '"':
                new_word += '!'
        new_message.append(new_word)
    new_message2 = []
    shift = 3  # величина смещения
    for word in new_message:
        x = shift % len(word)
        new_word = word[-x::] + word[0:-x]
        if '.' in new_word:
            shift += 1
        new_message2.append(new_word)
    new_text = ' '.join(new_message2)
    return new_text


if __name__ == '__main__':
    text = 'vujgvmCfb tj ufscfu ouib z/vhm jdjuFyqm jt fscfuu uibo jdju/jnqm fTjnqm tj scfuuf ibou fy/dpnqm yDpnqmf ' \
           'jt cfuufs boui dbufe/dpnqmj uGmb tj fuufsc ouib oftufe/ bstfTq jt uufscf uibo otf/ef uzSfbebcjmj vout/dp' \
           ' djbmTqf dbtft (ubsfo djbmtqf hifopv up csfbl ifu t/svmf ipvhiBmu zqsbdujdbmju fbutc uz/qvsj Fsspst' \
           ' tipvme wfsof qbtt foumz/tjm omfttV mjdjumzfyq odfe/tjmf Jo fui dfgb pg hvjuz-bncj gvtfsf fui ubujpoufnq' \
           ' up ftt/hv Uifsf vmetip fc pof.. boe sbcmzqsfgf zpom pof pvt..pcwj xbz pu pe ju/ Bmuipvhi uibu bzx bzn' \
           ' puo cf wjpvtpc bu jstug ttvomf sfzpv( i/Evud xOp tj scfuuf ibou /ofwfs uipvhiBm fsofw jt fopgu cfuufs' \
           ' boui iu++sjh x/op gJ ifu nfoubujpojnqmf tj eibs pu mbjo-fyq tju( b bec /jefb Jg fui foubujpojnqmfn jt' \
           ' fbtz up bjo-fyqm ju znb cf b hppe jefb/ bnftqbdftO bsf pof ipoljoh sfbuh efbj .. fu(tm pe psfn gp tf"uip'
    print(encrypt(text))
