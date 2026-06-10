# AI Assist Report

## The prompt I gave

<!-- How do I convert a Pandas column to datetime and replace invalid dates with missing values? -->

## The code it suggested

```python
sales["date"] = pd.to_datetime(
    sales["date"],
    errors="coerce"
)
```

## What I changed and why

<!-- I used the suggested code exactly as provided. I applied it to the date column in the sales DataFrame during the cleaning step. Using errors="coerce" converts invalid dates to NaT, which made it easy to identify and remove rows containing invalid dates later in the pipeline. -->

## Did it work?

<!-- Yes. The code successfully converted valid dates to the correct datetime format and replaced invalid dates with NaT. This simplified the data-cleaning process and showed how Pandas can handle date validation without writing custom parsing logic.-->
