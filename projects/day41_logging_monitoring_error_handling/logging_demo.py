
from logging_config import (
    configure_logging,
    LOG_DIR,
)


logger = configure_logging()


def main():

    print("\nDAY 41 — PART 1 LOGGING DEMO")

    logger.debug(
        "DEBUG: Detailed diagnostic message"
    )

    logger.info(
        "INFO: Application started successfully"
    )

    logger.warning(
        "WARNING: Example cache miss"
    )

    logger.error(
        "ERROR: Simulated operation failure"
    )

    try:
        result = 10 / 0

    except ZeroDivisionError:
        logger.exception(
            "EXCEPTION: Division operation failed"
        )

    print("\nLOG FILE:")
    print(LOG_DIR / "app.log")

    print("\nLOGGING DEMO COMPLETED")


if __name__ == "__main__":
    main()
