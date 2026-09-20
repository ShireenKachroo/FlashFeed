# FlashFeed

## MINIMAL ARCHITECTURE

                         ┌──────────────┐
                         │    User      │
                         └──────┬───────┘
                                │
                                ▼
                    ┌────────────────────┐
                    │     FastAPI        │
                    │   Backend/API      │
                    └─────────┬──────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
           PostgreSQL       Redis        AI/ML
                │                           │
                │                           │
                └─────────────┬─────────────┘
                              │
                              ▼
                       FlashFeed Feed