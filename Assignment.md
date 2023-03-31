**Short summary**

Your job is to create a simple backend-only application where an *investor* can *track* and *analyze* his *investments*.

**Description**

An investor can invest his money in different financial instruments. One of them are Loans, money borrowed to customers
or businesses. To simplify the situation, we’ll say that each loan has one single expected repayment (this is sometimes
called bullet repayment). This means that the investor invests some money in the loan (lends money to the
customer/business) and then expects a repayment on the maturity date of that loan.

**Main entities**

- Loan - contains the information of a loan in which the investor has invested.
- CashFlow - an event in the lifecycle of the loan.
    - We’ll consider two types of cash flows: funding, repayment

**Entities attributes**

|***Entity***|***Attribute***|***Type***|***Source***|***Description***|
| :- | :- | :- | :- | :- |
|<p></p><p>Loan</p>|identifier|string|Input|A unique identifier of the loan)|
||issue\_date|date|Input|The date in which the loan was created by the respective institution (bank etc.)|
||total\_amount|float|Input|The total amount of the loan |
||rating|integer|Input|The rating of the loan, from 1 to 9.|
||maturity\_date|date|Input|The date in which the repayment is expected.|
||total\_expected\_interest\_amount|float|Input|The total interest amount expected to be repaid on the maturity date
from the debtor.|
||invested\_amount|float|Calculated|The amount invested in the loan by the investor|
||investment\_date|date|Calculated|The date in which the investment was placed.|
||expected\_interest\_amount|float|Calculated|The interest amount expected to be repaid to the investor on the maturity
date.|
||is\_closed|boolean|Calculated|Indicates if the investment is still completed, or it is still open.|
||expected\_irr|float|Calculated|The expected Internal Rate of Return, a percentage indicating the expected return
rate. |
||realized\_irr|float|Calculated|The Internal Rate of Return, calculated when the investment is closed. |
|<p></p><p>CashFlow</p>|loan\_identifier|string|Input|The identifier of the loan to which this cash flow is related.|
||reference\_date|date|Input|The date in which the event happened|
||type|string|Input|Funding/Principal Repayment/Interest Repayment|
||amount|float|Input|The amount funded/repaid.|

**Fields calculation:**

1. investment\_date
    1. Calculated only when the loan is created.
    1. Equal to the reference\_date of the funding cash flow of the loan.
1. invested\_amount
    1. Calculated only when the loan is created.
    1. Equal to the amount of the funding cash flow of the loan.
1. expected\_interest\_amount
    1. Calculated only when the loan is created.
    1. total\_expected\_interest\_amount \* (invested\_amount / total\_amount)
1. is\_closed
    1. Calculated whenever a new cash flow for the loan is received.
    1. If the loan has received a total repaid amount equal to the expected amount (invested\_amount +
       expected\_interest\_amount) or higher, it is considered closed. Otherwise it is still open.
1. expected\_irr
    1. Calculated only when the loan is created.
    1. Use the XIRR function for this purpose.
    1. *Hints:*
        1. IRR is a percentage, representing the rate of return of the investment.
        1. You can use the XIRR function from any Python library or any implementation on the web.
        1. The XIRR function takes an array of (date, amount) tuples, representing cash flows (realized or expected) and
           returns a float between 0 and 1.
        1. For the expected IRR, the cash flows that should be used are:
            1. The funding
                1. date: reference\_date
                1. amount: funding amount (negative)
            1. The expected repayment:
                1. date: maturity\_date
                1. amount: invested\_amount + expected\_interest\_amount (positive)
1. realized\_irr
    1. Similar to the expected\_irr
    1. Calculated only when the loan is closed.
    1. The cash flows that should be used are:
        1. The funding
            1. date: reference\_date
            1. amount: funding amount (negative)
        1. The repayment
            1. date: reference\_date
            1. amount: repayment amount (positive)

**Functional Requirements**

- Allow the user to upload the data of his investments in the application.
    - When doing this, the user will provide 2 CSV files:
        - One containing the loans.
        - One containing the cash flows of the loans.
    - Calculate the loan fields as necessary.
- Allow the user to create a repayment for a loan, not through the CSV file.
    - The necessary loan calculations should take place in this case as well.
- Allow the user to view his loans and filter them by any attribute.
- Allow the user to view the cash flows and filter them by any attribute.
- Allow the user to view statistics on his investments:
    - Number of Loans
    - Total invested amount (all loans)
    - Current invested amount (only open loans)
    - Total repaid amount (all loans)
    - Average Realized IRR
        - Weighted average of realized IRR, using the loan invested amount as weight.
        - Consider only closed loans.

**Other Requirements**

- The application should expose a REST API for the required functionalities.
- The application should support authentication and authorization.
    - 2 types of users:
        - Investor - Can do anything on the application.
        - Analyst - Read-only permissions.
- The processing of the CSV files should happen asynchronously.
- The statistics should be stored in a cache.
    - Whenever new loans/cash flows arrive, the cache should be invalidated.
- The project should be set up with the usage of docker and docker-compose.

**Technologies:**

- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [drf-spectacular](https://github.com/tfranzel/drf-spectacular)
- [Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html)
- [Redis](https://github.com/jazzband/django-redis)
- [docker + docker-compose](https://docs.docker.com/)

**Example files:**

- loans.csv
- cash\_flows.csv

