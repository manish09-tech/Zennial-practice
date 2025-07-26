import logging

# Configure the logger
logging.basicConfig(
    filename="user.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger("UserLogger")
