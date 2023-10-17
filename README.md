# SocialDjango
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![DjangoRestFramework](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
## Description
This is a social network, several of its main features are mentioned below

- Share the post with comment and like
- system followings and follower
- Giving suggested posts to each user
- Chat realtime (later)
- Revenue system(later)

## Installation
```commandline
docker-compose up -d
```

#### create SuperUser
```commandline
docker exec -it social-application python manage.py createsuperuser
```

### Schema

| Type      | EndPoint     |
|-----------|--------------|
| File      | api/schema/ |
| swager ui | api/schema/swagger-ui/ |
| redoc ui  | api/schema/redoc/ |

## NOTE
I will be happy if report problem or send pull request for better code
