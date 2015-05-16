---
layout: post
title: Custom Russian WordList Generator
---

**TL;DR**
This is a generator of custom russian dictionaries, based on reverse translit, and basic password analyzer.

You can download tool [here](https://github.com/lctrcl/crwg)

# Intro

Lately there were many reports of password breaches in big resources, such as mail.ru, yandex.ru and so on. One can easily find them on the Internet. Resource [haveibeenpwned.com](https://haveibeenpwned.com) by Troy Hunt keeps track of the latest breaches.

These leaks are of great interest to information security researchers.
We have great tools to analyze these dumps, such as [pipal](https://digi.ninja/projects/pipal.php) by @digininja, but none of them have ability to analyze password through one principle I am describing below.

# Russian 'reverse translit' principle 

Many russian-speaking people use dictionary passwords, but based on 'reverse translit' (I don't know what really term is, just using this to refer to such principle). Basically when you have dual-layout keyboards such as following, you write russian words in english layout.
![this](http://www.thebrainfever.com/images/kb/KB_0024_Russian.png)

So if English-speaking people look on these passwords, they look like gibberish:
- ghbdtn
- gfhjkm
- etc.

They are actually russian words written in 'reverse translit':
- привет
- пароль
- и т.д.

Current tools doesn't have ability to find this kind of passwords, so I wrote a little Python tool over a weekend to accomplish this.

It's called "Custom Russian WordList Generator" and it does basically three things:
- downloads and cleans up russian dictionary (based on ruscorpora and opencorpora)
- generates custom dictionaries in 'reverse translit'
- analyzes passwords leaks (not provided) and finds frequency of such passwords

It can be easily extended with new layouts and have also clasical 'translit' mode.
In the future I might convert it to pipal module (if it's possible).

# Where it's useful

In pentest, it's always useful to generate custom wordlists. With a combination of [CeWl](https://digi.ninja/projects/cewl.php) and CRWG you can build up some nice wordlists if you working with russian-based companies and persons. 

Also, you can just take top used 'reverse translit' passwords and use it at a custom dictionary.

# Usage

`git clone https://github.com/lctrcl/crwg`
`pip install -r requirements.txt`

Download and clean up russian dictionaries:

    python crwg.py --downloaddictionaries ruscorpora --autoclean

Generate dictionary:

    python crwg.py -g ru_inv_en -s ruscorporadict_stripped -d ruscorporadict_stripped_ru_inv_en

Generate statistics:

    python crwg.py -c --source 'someleakedpasswords' -d ./statistics --dictionary ruscorporadict_stripped_ru_inv_en

## Help

    usage: crwg.py [-h] [--gendic {ru_inv_en,translit,tran5l1t}]
               [--downloaddictionaries {ruscorpora,opencorpora}] [--autoclean]
               [--source SOURCE] [--destination DESTINATION]
               [--dictionary DICTIONARY] [--compare_two_password_bases]
    Custom Russian Wordlists Generator 0.3
    optional arguments:
      -h, --help            show this help message and exit
      --gendic {ru_inv_en,translit,tran5l1t}, -g {ru_inv_en,translit,tran5l1t}
                            Generate dictionary from file
      --downloaddictionaries {ruscorpora,opencorpora}
                            Download ruscorpora or opencorpora
      --autoclean           Autoclean downloaded dictionaries (english characters,
                            numbers, etc)
      --source SOURCE, -s SOURCE
                            Source file
      --destination DESTINATION, -d DESTINATION
                            Destination file
      --dictionary DICTIONARY
                            Dictionary file
      --compare_two_password_bases, -c
                            Compare two password files
    Usage: python crwg.py -g ru_inv_en -s sourcedict -d destinationdict /or/
    python crwg.py --downloaddictionaries ruscorpora --autoclean /or/


# Analysis of passwords

For analysis I took mail.ru, yandex.ru, gmail and sprashivai dumps.

Overall it was 26212007 passwords in these dump.
There was 337767 passwords based on 'reverse translit' principle so it was ~1,28% of all the passwords combined.

Top-20 passwords are (count - password - russian word - english word translated):

    5421    gfhjkm         пароль       (password)
    4674    ghbdtn         привет       (hello)
    2409    fyfcnfcbz      анастасия    (Anastasiya)
    2168    rhbcnbyf       кристина     (Kristina)
    2157    vfrcbv         максим       (Maksim)
    2000    rfrfirf        какашка      (poop/shit)
    1863    vfhbyf         марина       (Marina)
    1836    vfvjxrf        мамочка      (mommy)
    1753    cjkysirj       солнышко     (sunny)
    1663    dbrnjhbz       виктория     (Victoria)
    1660    yfnfif         наташа       (Natasha)
    1634    cghfibdfq      спрашивай    (sprashivai)
    1630    ghbdtnbr       приветик     (hello there)
    1498    fylhtq         андрей       (Andrei)
    1405    fktrcfylh      александр    (Alexander)
    1362    trfnthbyf      екатерина    (Ekaterina)
    1266    k.,jdm         любовь       (love/Lyubov)
    1214    ybrbnf         никита       (Nikita)
    1159    hjvfirf        ромашка      (camomile)
    1055    ghjcnj         просто       (just/simply)

As you see, nothing surprising - 'password' is the top one.
A lot of users use their first names as the password. Password 'k.,jdm' can be interpreted as a word 'love' or female name 'Lyubov'.

The password 'спрашивай' is the name of service (sprashivai.ru) was the most popular of all services - 1634. For example, password 'zyltrc' (yandex) was used 80 times, 'zyltrche' (yandex.ru) - 3, 'vtqkhe' (mail.ru) - 4
Suprisingly, password 'drjynfrnt' (vkontakte), popular russian social service, was used 766 times.

Let's take russian names dictionary and look at top-20 names:

    2409    fyfcnfcbz   анастасия       (Anastasiya)
    2168    rhbcnbyf    кристина        (Kristina)
    2157    vfrcbv      максим          (Maksim)
    1863    vfhbyf      марина          (Marina)
    1498    fylhtq      андрей          (Andrey)
    1405    fktrcfylh   александр       (Alexander)
    1362    trfnthbyf   екатерина       (Ekaterina)
    1266    k.,jdm      любовь          (Lyubov)
    1214    ybrbnf      никита          (Nikita)
    997     nfnmzyf     татьяна         (Tatyana)
    989     fktrctq     алексей         (Alexey)
    937     cthutq      сергей          (Sergey)
    890     dthjybrf    вероника        (Veronika)
    858     lvbnhbq     дмитрий         (Dmitry)
    856     rfhbyf      карина          (Karina)
    810     cdtnkfyf    светлана        (Svetlana)
    766     gjkbyf      полина          (Polina)
    744     rbhbkk      кирилл          (Kirill)
    681     fyutkbyf    ангелина        (Angelina)
    668     dfkthbz     валерия         (Valerya)

Top-20 locations (cities,countries):

    338     hjccbz          россия            (Russia)
    256     vjcrdf          москва            (Moscow)
    192     vflfufcrfh      мадагаскар        (Madagascar)
    136     erhfbyf         украина           (Ukraine)
    128     cfvfhf          самара            (Samara)
    126     vfhctkm         марсель           (Marseille)
    100     djkujuhfl       волгоград         (Volgograd)
    96      fvcnthlfv       амстердам         (Amsterdam)
    88      ctdfcnjgjkm     севастополь       (Sevastopol)
    85      kjyljy          лондон            (London)
    85      rfhfufylf       караганда         (Karaganda)
    78      lytghjgtnhjdcr  днепропетровск    (Dnipropetrovsk)
    76      fynfyfyfhbde    антананариву      (Antananarivu)
    73      bcgfybz         испания           (Spain)
    72      vfyxtcnth       манчестер         (Manchester)  
    69      ahfywbz         франция           (France)
    68      ,fhctkjyf       барселона         (Barcelona)
    67      rfpfym          казань            (Kazan)
    65      uthvfybz        германия          (Germany)
    58      fdcnhfkbz       австралия         (Australia)

Surprisingly, Madagascar is Top-3 password (I have no explanation to this).
Password 'vfhctkm' (Marseille) can also be a male name.
Password 'fynfyfyfhbde' (Antananarivu) is suprising, but it's more not due popularity of place itself, but due to song "Antananarivu" by russian pop-star Zemfira.
Passwords of 'manchester' and 'barcelona' are also traditionally considered football-related due to overall popularity of MU and Barcelon FC.

# misc

Twitter: @lctrcl
Github: github.com/lctrcl
