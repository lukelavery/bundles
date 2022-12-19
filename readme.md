<h1 align="center">AG Bundle Tool</h1>

<h4 align="center">A desktop application that automates the bundling of pdf documents for use in court proceedings.</h4>

## Key Features

* Producing an index
* Merging documents
* Pagination
* Hyperlinking

## How to use

This software relies on good file management practices and follows specific conventions to automate the bundling process. A correctly formatted example can be found in the example directory.

#### File Structure

Your files should be organised as follows

```
parent_folder
│   index_template.docx  
│
└───folder1
│   │   file1.pdf
│   │   file2.pdf
│   
└───folder2
    │   file3.pdf
    │   file4.pdf
    │   ...
    ...
```
* 'parent_folder': this is the root folder that contains all the files for your bundle. This is the folder you will select in the application to load your files.
* 'index_template.docx' - this is an optional template document that allows you to include header information in the generated index. It must be located within *'parent_folder'*. If this document is not included, a blank document will be used to generate the index.
* 'folder1', 'folder2' etc., etc.: these subfolders correspond to the sections in the generated index. All documents in the bundle must be included inside subfolders within 'parent_folder'.
* 'file1.pdf', 'file2.pdf', etc.: these are the individual entries in the bundle. They must be pdf documents.

#### Naming conventions

* 'parent_folder' - this will be the name of your bundle and can be changed to anything
* 'index_template.docx' - the name of this documents must not be changed or the software will resort to a blank word document to generate your index.
* 'folder1', 'folder2' etc. - the subfolders should be named in the following format:
  * 'A. [Section Name]'
  * 'B. [Section Name]'
  * ...
* 'file1.pdf', 'file2.pdf' etc. - these files should be names in the following format:
  * '[YYYY.MM.DD] - [Document Name]'
 

## Credits

This software uses the following open source packages:
* [PyPDF2](https://pypdf2.readthedocs.io/en/latest/)
* [python-docx](https://python-docx.readthedocs.io/en/latest/)
* [pdfminer.six](https://pdfminersix.readthedocs.io/en/latest/)
* [The ReportLab Toolkit](https://www.reportlab.com/)
* [docx2pdf](https://github.com/AlJohri/docx2pdf)
