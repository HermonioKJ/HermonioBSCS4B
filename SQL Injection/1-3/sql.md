##Subverting application logic part 3

if you log in in username without a password you can comment -- to erase the password condition

#Theory
administrator'--

SELECT * FROM users WHERE username = 'administrator'--' AND password = ''


