# Code example
__example with using Docker, UnitTests and DRF__

Скопируйте к себе проект и выполните команду `sudo docker-compose up`

`/accounts/registration/` POST email, password - регистрация пользователя

`/accounts/transaction/` POST sender, recipient, amount, wallet - перевод денег от sender к recipient

`/accounts/transaction/` GET user_id - история транзакций пользователя

