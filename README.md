# Job Vacancy Analysis

This project analyzes job vacancies from the dou.ua website, including visualizations to better understand trends in the job market for developers. We use Python and libraries such as pandas, matplotlib, and seaborn for data processing and visualization.

# Features
* Data Loading and Preprocessing: Load job vacancies from a CSV file, clean and preprocess the data, and handle missing values (e.g., filling missing experience or salary data).
* Visualizations:
    * Vacancies by Company: A bar chart displaying the number of job vacancies available per company.
    * Vacancies by Technology: A bar chart showing the most popular technologies mentioned in job vacancies.
    * Vacancies by Experience: A bar chart visualizing the distribution of job vacancies based on required experience levels.
* Salary Analysis: Visualizations based on salary data, including salary distribution by experience and other categories.
* Customizable: Easily customizable for other datasets or job vacancy sources by modifying the input CSV file.

# Example of result graphs
1. Number of Vacancies by Company
   This bar chart shows which companies are actively seeking developers. Vacancies are grouped by company.

![top_10_companies.png](top_10_companies.png)


2. Number of Vacancies by Technology
   This graph displays the most popular technologies among employers seeking developers.

![vacancies.png](vacancies.png)


3. Number of Vacancies by Experience
   This chart shows how many vacancies are open for different experience levels, helping to understand which experience categories are most in demand.

![vacancies_for_experience.png](vacancies_for_experience.png)


## Installation
1. * Clone the repository to your local machine:
   ```bash
    git clone https://github.com/Sergi0bbb/scrape-and-analyze.git
    cd scrape-and-analyze
    python -m venv venv
    pip install -r requirements.txt
2. * Configure Environment:
      * Use .env.sample to configure your DB_NAME and TABLE_NAME.
3. Run script:
    ```bash
    scrapy crawl dou

4. * Running the Analysis:
     * After scraping the data, execute the data export and analysis scripts — dou_analysis.ipynb. The analysis script will produce visualizations, including bar charts illustrating hiring trends and

