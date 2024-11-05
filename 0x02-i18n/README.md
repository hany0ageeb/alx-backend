# 0x02. i18n
## Resources
### Read or watch:
- [Flask-Babel](https://web.archive.org/web/20201111174034/https://flask-babel.tkte.ch/)
- [Flask i18n tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-i18n-and-l10n)
- [pytz](https://pypi.org/project/pytz/)
## What Is i18n?
Internationalization, prepares your software for worldwide use. This process separates locale and language details from the main code, enabling support for various languages and cultural norms efficiently and cost-effectively.

Internationalization (i18n) is the process of designing and developing software so it can be adapted for users of different cultures and languages.

Internationalization (i18n) is the process of designing and developing a software product so it can be adapted for users of different cultures and languages.

Internationalization doesn’t just involve enabling different languages—it also entails adapting the software to accept different forms of data and settings to match local customs and process them correctly.

**Internationalization usually includes:**

- Designing and developing in a way that removes barriers to localization or international deployment. This includes such things as enabling the use of Unicode, ensuring the proper handling of legacy character encodings where appropriate, taking care over the concatenation of strings, avoiding dependence in code of user-interface string values, etc.

- Providing support for features that may not be used until localization occurs. For example, adding markup in your DTD to support bidirectional text, or for identifying language. Or adding to CSS support for vertical text or other non-Latin typographic features.

- Enabling code to support local, regional, language, or culturally related preferences. Typically, this involves incorporating predefined localization data and features derived from existing libraries or user preferences. Examples include date and time formats, local calendars, number formats, and numeral systems, sorting and presentation of lists, handling of personal names and forms of address, etc.

- Separating localizable elements from source code or content, such that localized alternatives can be loaded or selected based on the user’s international preferences as needed.