# task-1

Project Management System Technology - Python (Django/ Flask)
APIs :

    Manage users (Register/login)
    Manage projects (CRUD)
    Manage tasks (CRUD)
    Owner of the project can share that project with other users(if user is active) based on permission (Edit, Delete, View)
    Only Project owner should be able to create tasks

Tables:

    User (id, username, name, password)
    Project (id UUID, name, desc, created_by, created_at, project_color_identity)
    Tasks (id, task_name, description)
    Permission (id, name, description)

Note:

    Identify the primary key and use the appropriate foreign key as per need, You can also add more tables as per need.
    One project can have multiple tasks
    If user have "View" Permission then that user can also see the project but not able to update or delete that project or tasks.
