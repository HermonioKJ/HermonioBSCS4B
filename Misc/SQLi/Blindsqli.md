##dificulty hard
##Blind SQL injection

go to:https://primer.picoctf.org/vuln/web/blindsql.php

if you input ' or '1'='1 in a password field and submit
it shows the result of register found

this means that the text field is vurnerable to sql attack

now we guess the username as picoctf

so we input in a password textfield ' or username='picoctf

if the label register says register found that means that user picoctf exist

Remember that in our injection, if the part at the right of the "or" is true,
it will return results. It is true that username is equal to 'picoctf'
only in the row on the picoctf!

Now we will add the part that compares the first character of the password.
We can do that using an embedded query. An embedded query is a
query inside a query. Our embedded query highlighted in green,
will simply return the first character of the password.
We will compare that first character with the character 
'a', so we are guessing that the first character is 'a':

what this code does is you try to guess the first letter of the password
' or username='picoctf' and (select substr(password, 1,1))='a

if nothing founds that means that in a first word of your password doesnt
contains letter a

if you do this. it could take you 1 day just to guess the password we will
let python do it for us.

look in the same directory..
