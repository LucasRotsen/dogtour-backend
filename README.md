# DogTour
DogTour é uma plataforma cujo objetivo é facilitar o agendamento de passeios com cães. O projeto foi desenvolvido como requisito para aprovação na disciplina Trabalho Interdisciplinar de Software V, que teve como "disciplinas antenas" Gerência de Projetos, Arquitetura de Software e Desenvolvimento de Aplicações Móveis e Distribuídas. A nossa solução envolve, no frontend, uma SPA (single-page application) desenvolvida em Ionic e, no back-end, microsserviços escritos em Python. Além disso, utilizamos o protocolo de fila de mensagens AMQP (RabbitMQ) como middleware de comunicação indireta para o sistema.

<br>

![Arquitetura do Projeto](misc/architecture.png?raw=true "Title")

<br>

Foram criados dois repositórios para o sistema, um para o [Front-end](https://github.com/RafaelBadaro/dogtour.git) e outro para o [Back-end](https://github.com/LucasRotsen/dogtour-backend.git).

<br>

## Executando o projeto

### Back-end

Para executar o Back-end do projeto basta executar o seguinte comando:

    $ docker-compose up

