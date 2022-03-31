When you run `filter.py`, you should be greeted with an infinite loop that prompts you for a query string.

For the query string, you can frame it as a series of search strings separated by `,`. For example, to search for a dialogue that contains both `alpha milton guest house` and `tuesday`, you can use `alpha milton guest house,tuesday`.

This will return a list of dialogue IDs, which you can then use to manually sift through the `data.json` file to find the associated dialogue.
