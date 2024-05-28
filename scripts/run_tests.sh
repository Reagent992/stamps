ENV_ACTIVATE=$(grep ENV_ACTIVATE .env | cut -d '=' -f2)
source $ENV_ACTIVATE && python src/manage.py test src
