TEST_CASES = [
    {
        "id": "annual_leave_days",
        "question": (
            "How many annual leave days "
            "do employees get?"
        ),
        "expected_status": "answered",
        "expected_source": "leave_policy.txt",
        "expected_answer_groups": [
            ["24"],
        ],
    },

    {
        "id": "leave_carry_forward",
        "question": (
            "How many unused leave days "
            "can be carried forward?"
        ),
        "expected_status": "answered",
        "expected_source": "leave_policy.txt",
        "expected_answer_groups": [
            ["5", "five"],
        ],
    },

    {
        "id": "long_leave_approval",
        "question": (
            "Who must approve leave lasting "
            "more than five consecutive working days?"
        ),
        "expected_status": "answered",
        "expected_source": "leave_policy.txt",
        "expected_answer_groups": [
            ["manager"],
        ],
    },

    {
        "id": "contractor_paid_leave",
        "question": (
            "Can contractors take paid annual leave?"
        ),
        "expected_status": "answered",
        "expected_source": "contractor_policy.txt",
        "expected_answer_groups": [
            ["no", "not eligible"],
        ],
    },

    {
        "id": "contractor_unpaid_time_off",
        "question": (
            "Can contractors request unpaid time off?"
        ),
        "expected_status": "answered",
        "expected_source": "contractor_policy.txt",
        "expected_answer_groups": [
            ["yes", "may", "can"],
        ],
    },

    {
        "id": "remote_work_days",
        "question": (
            "How many days per week can employees "
            "work remotely?"
        ),
        "expected_status": "answered",
        "expected_source": "remote_work_policy.txt",
        "expected_answer_groups": [
            ["3", "three"],
        ],
    },

    {
        "id": "permanent_remote_approval",
        "question": (
            "Who must approve a permanent "
            "remote work arrangement?"
        ),
        "expected_status": "answered",
        "expected_source": "remote_work_policy.txt",
        "expected_answer_groups": [
            ["manager"],
            ["human resources", "hr"],
        ],
    },

    {
        "id": "password_length",
        "question": (
            "What is the minimum password length?"
        ),
        "expected_status": "answered",
        "expected_source": "it_security_policy.txt",
        "expected_answer_groups": [
            ["12", "twelve"],
        ],
    },

    {
        "id": "multi_factor_authentication",
        "question": (
            "Is multi-factor authentication "
            "mandatory?"
        ),
        "expected_status": "answered",
        "expected_source": "it_security_policy.txt",
        "expected_answer_groups": [
            ["yes", "mandatory"],
        ],
    },

    {
        "id": "relocation_allowance",
        "question": (
            "What is the company's "
            "relocation allowance?"
        ),
        "expected_status": "insufficient_evidence",
        "expected_source": None,
        "expected_answer_groups": [],
    },

    {
        "id": "health_insurance",
        "question": (
            "How much does the company pay "
            "for employee health insurance?"
        ),
        "expected_status": "insufficient_evidence",
        "expected_source": None,
        "expected_answer_groups": [],
    },

    {
        "id": "cafeteria_hours",
        "question": (
            "What time does the company "
            "cafeteria open?"
        ),
        "expected_status": "insufficient_evidence",
        "expected_source": None,
        "expected_answer_groups": [],
    },
]