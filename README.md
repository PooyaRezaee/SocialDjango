# SocialDjango

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
