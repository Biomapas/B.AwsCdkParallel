class RetryableIndicators:
    """
    A class that holds a bunch of indicators that indicate that a stack deployment can be retried.
    For example, if your stack deployment fails with an exception, get the stack trace, compare
    against these indicators and if any of them matches - you're safe to retry!
    """
    INVALID_CHANGESET_STATUS_INDICATORS = [
        'failed: InvalidChangeSetStatus: Cannot delete ChangeSet in status CREATE_IN_PROGRESS',
        'code: \'InvalidChangeSetStatus\''
    ]

    ALL_INDICATORS = [
        INVALID_CHANGESET_STATUS_INDICATORS
    ]
