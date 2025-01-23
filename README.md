# news-to-reel
B-tech final project.

## Setup

To run the web app in your machine, download the code ZIP file or clone this repository.<br>
Open a terminal and change directory to `news-to-reel`.
```bash
git clone https://github.com/AutoMarkGraders/news-to-reel.git
cd news-to-reel
```

### 1. Front-end

- **Node.js**: Download and install version 14 or newer from [Nodejs.org](https://nodejs.org/).
- Install dependencies and Run the server using the commands:
    ```bash
    cd pages
    npm install
    npm run dev
    ```
    The react app will be running at `http://localhost:5173`. Access it using a web browser.

### 2. Database

- **PostgreSQL**: Download version 13 or newer from [PostgreSQL.org](https://postgresql.org/). Install all the components during the installation.
- **Password**: During installation, set the database superuser(postgres) password as `root`. If you want to use another password, define it in the .env file.
    ```bash
    database_password=your_database_superuser_password
    ```
<!-- - **Create server**: Open pgAdmin 4 and click on `Server` -> `Register Server`. Set Name as `local postgres`, Host name as `localhost`. Use same password as before. Click Save. -->
- **Access server**: Open pgAdmin4 and click on `Servers` from the left sidebar. Access the existing server (eg- `PostgreSQL 18`) using the password from before.
- **Create database**: Right click on `Databases` -> `Create` -> `Database`. Set Database name as `ntr`. Click Save.
- **Create tables**: Right click on `ntr` -> `Query Tool`. Copy & paste the below queries one by one and execute by pressing `F5`:
    ```bash
    CREATE TABLE IF NOT EXISTS public.users
    (
        id serial NOT NULL,
        email character varying(25) COLLATE pg_catalog."default",
        password character varying COLLATE pg_catalog."default" NOT NULL,
        created_at timestamp with time zone NOT NULL DEFAULT now(),
        CONSTRAINT users_pkey PRIMARY KEY (id),
        CONSTRAINT users_email_key UNIQUE (email)
    )
    TABLESPACE pg_default;
    ALTER TABLE IF EXISTS public.users
        OWNER to postgres; 
    ```

### 3. Back-end

- **Python**: Download and install a version between 3.8 and 3.11 from [Python.org](https://python.org/). Check Python & pip installation:
    ```bash
    python --version
    pip --version
    ```
- **Dependencies**: Install the required Python packages listed in `requirements.txt`:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```
- **ImageMagick**: Download and install from [imagemagick.org](https://imagemagick.org/script/download.php). Make sure IMAGEMAGICK_BINARY is correct at line 3 of backend/app/generator.py.
- **Download Models**: From [here](https://drive.google.com/drive/u/1/folders/1BF9CSPRBQB7KL7TD9xtuHEZKyx0ukT7Y) download model.safetensors for backend/app/saved_classifier and backend/app/saved_summarizer.
- **Start server**: Run the FastAPI backend with uvicorn. The server will start on `http://localhost:8000`.
    ```bash
    uvicorn app.main:app --reload
    ```


## API endpoints details

After starting the FastAPI server with uvicorn, go to `http://127.0.0.1:8000/docs` to see the request and response associated with each endpoints.
