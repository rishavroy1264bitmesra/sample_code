# Document Hierarchy Identification

*Project* identifies document hierarchy layout.

## Code Design Flow in Execution Order
1. Web Service :`app.py`
2. Executors : `src/pipeline_executor.py`
3. HTML Splitter and Reader: `src/html_splitter.py` and `src/html_line_parser.py`
4. Classifiers: `src/classifiers_executor.py`
5. Validators: `src/validators_executor.py`
6. Response Generators: `src/json_gen_executor.py`

## Model Training Flow
1. `classifiers` package consists of training/testing/classification logic and algorithms.
2. `datasets` directory consists of all training dataset for each models.
3. `models` package holds the trained and saved models.
4. `feature_extractors` package holds custom engineered features for respective classifiers.
5. `lookup_dictionaries` package holds keyword based features.

## Code Utilities
1. `bullet_templates` : Implementation of *Strategy Design Pattern*, to find bullet style of a text.
2. `objects` : Python Object Classes, used while, JSON Response Generation.
3. `tests` : Unit Tests for *Document Hierarchy Identification* Code.
4. `utils` : holds CONSTANTS and other utility methods.
5. `setup_log.py` : logging configuration file loader.
6. `logConfig.yaml`: logging configuration file, used throughout the Code.

## Endpoints
1. `/holmes4business/contract_intel/v2/sectionExtract` : External API for Paragraph Extraction
2. `/holmes4business/contract_intel/v2/flatResponse` : Internal Usage Purpose to View the FlatResponse
3. `/holmes4business/contract_intel/v2/lineidsResponse`: External API for Paragraph Extraction with sub_section level lineids.
4. `/holmes4business/contract_intel/v2/htmlResponse`: External API accepts input html and returns `<h1>` and `<h2>` tags added to html after identifying headings and subheadings.

## Input

Input to the REST API is html content of file as `body` and key as `Client` and following values for client in header.

Based on passed Client, dynamically models and client specific features are executed in pipeline.

Following are permissible values for clients:

1. `erm` to process erm files
2. `t_mobile` to process t_mobile files
3. `isda` to process isda files
4. `bestbuy` to process bestbuy files
5. `generic` to process any new file.

Note: If no `Client` is passed in headers, by default loads `generic` models.

## Internal Helper API's

1. `helpers/bulk_json_generator.py` : Internal API to process in bulk html files for paragraph extraction. Needs `folder_path` of html files and `Client`.Generates and writes `JSON Response`.
2. `helpers/bulk_excel_generator.py` : Internal API to process in bulk html files for paragraph extraction. Needs `folder_path` of html files and `Client`.Generates and writes `Excel_Response`.
3. `helpers/bulk_doc_title_extractor.py`: Internal API to process in bulk html files for document title extraction. Needs `folder_path` of html files and `Client`.Generates and writes `Excel_Response`.
4. `helpers/model_dataset_evaluator.py`: Evaluator to evaluate custom model on custom dataset. generates Precision, Recall and F1 scores.
5. `helpers/bulk_doctype_runner.py`: Internal API to process in bulk ocr htmls and generate docType htmls.
6. `helpers/bulk_html_generator.py`: Internal API to process in bulk input htmls and converts them to htmls having `<h1>` tag for heading, `<h2>` tag for subheading.
7. `helpers/bulk_ocr_runner.py`: Internal API to process in bulk pdfs to OCR and generate htmls.
## Output

Returns JSON response, consists of following JSON keys:
1. `Paragraphs` : holds the content of posted document in structured format.
2. `Document_Titles`: holds the identified document title.
3. `others`: holds the filtered out texts while generating document structured format.

## Sample Response

    {
        "Paragraphs": [{
                "Clause": {
                    "Main-heading": "SITE LEASE AGREEMENT",
                    "Sub-heading": "1. Property Description .",
                    "Sub-section": [
                        " Landlord is the owner of the real property located at Error! Reference source not found. , Error! Reference source not found. as further described on Exhibit A (the Property ). The Property includes the premises which is comprised of approximately Error! Reference source not found. square feet plus any additional portions of the Property which Tenant may require for the use and operation of its facilities as generally described on Exhibit B (the Premises ). Tenant reserves the right to update the description of the Premises on Exhibit B to reflect any modifications or changes."
                    ]
                },
                "Page_Style": "width:815.79596px;height:1055.736px;overflow:hidden;",
                "Document_Type": "exhibit",
                "Bottom_Right": "top:327.82468px;left:336.27863px",
                "Top_Left": "top:230.2091px;left:90.08947px",
                "Page_Number": "['page_0']",
                "Tag_No": "['11', '12', '13', '14', '15', '16', '17', '18', '19', '20']",
                "File_Name": "\n   Standard_Lease_Template.pdf\n  ",
                "Priority": "5"
            }]
    }

