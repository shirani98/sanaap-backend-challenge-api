# Architecture

## Stack
Django 5 · DRF · SimpleJWT · drf-spectacular · django-storages (MinIO) · PostgreSQL · Redis

## App layout
```
apps/
├── records/          # Data record domain
│   ├── models/       # DataRecord model
│   ├── selectors/    # Read-only queries
│   ├── services/     # Write operations + validation
│   └── api/
│       ├── serializers/
│       ├── views/    # One class per action
│       └── urls.py
├── user/             # Auth & identity
│   ├── models/       # Custom User (AbstractUser)
│   ├── api/views/    # LoginView, RefreshTokenView, LogoutView
│   ├── signals.py    # Creates role groups on post_migrate
│   └── management/commands/setup_roles.py
└── utils/
    ├── responses/    # BaseResponse
    ├── filters/      # DataRecordFilter
    ├── pagination/   # StandardResultsPagination
    ├── permissions/  # IsAdmin, IsEditorOrAdmin, IsAnyRole
    └── storage/      # MinIOStorage
```

## Request flow
```
Request → View → Permission check → Serializer → Service/Selector → DB → BaseResponse
```

## RBAC
| Group | add | change | delete | view |
|-------|:---:|:------:|:------:|:----:|
| admin | ✅ | ✅ | ✅ | ✅ |
| editor | ✅ | ✅ | ❌ | ✅ |
| viewer | ❌ | ❌ | ❌ | ✅ |

Groups are created automatically on `migrate` via `post_migrate` signal.
