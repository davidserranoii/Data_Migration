<h1>Data Migration Tools</h1>

<p>This repository contains a few tools that I created in my off time to help me with my daily tasks in data migration. Each tool is designed to help meet a specific need in data migration relative to my job duties. I no longer have a need for these tools but welcome anyone to use this repository. I personally just love scripting. The rest of this document will be used for a brief introduction, outline requirements for the tools, and offer a quick How-To.</p>

<h2>Tools</h2>
<ul>
  <li><strong>BulkLoadSSMS.py:</strong> Import multiple csv files into SSMS with a few inputs.</li>
  <li><strong>Compare_Columns.py:</strong>Select two csv files to compare. The script will return columns that don't match, and columns that exist within one and not the other.</li>
  <li><strong>Excel_to_CSV.py:</strong>Select an xlsx file with multiple tabs. The script will separate each sheet into an individual csv linked together by the input you provide.</li>
</ul>

<h3>BulkLoadSSMS.py</h3>
<h4>Prerequisites</h4>
<p><strong>Libraries Used</strong></p>
<ul>
  <li>os</li>
  <li>pyodbc</li>
  <li>pandas</li>
  <li>socket</li>
</ul>

<p><strong>Required Setup</strong></p>
<ul>
  <li>Must be a Windows Operating System</li>
  <li>Importing files must all be csv's</li>
  <li>SSMS must be running</li>
  <li>The table must already exist within SSMS</li>
  <li>SSMS Server type: Database Engine</li>
  <li>SSMS Server name: "yourhostname"\SQLEXPRESS</li>
  <li>SSMS Authentication: Windows Authentication</li>
</ul>

<p><strong>Using the tool: BulkLoadSSMS</strong></p>
<ol>
  <li>Create an empty database within SSMS, be sure to remember the table name.</li>
  <li>Run the BulkLoadSSMS script.</li>
  <li>The input "What is the file path for the files you wish to load?" requires the full path to the <em>folder</em> holding the files to import. Ex: C:\Users\billyJoel\Desktop\Excel_Ex.</li>
  <li>The input "What is the Database Name:" requires the database name that you created. This is case sensitive, and may also struggle with special characters or spaces.</li>
  <li>While the script is running, it will print the top 5 records of the document and ask if it looks good. Type "Y" or "y" and press enter to import, and anything else to skip import.</li>
  <li>If the table already exists, it will ask if you want to drop the existing table, type "Y" or "y" for yes, and no to cancel the import.</li>
  <li>The script should be finised at this point, the final output shows files imported by their full file path, and the files not imported in a list [] format.</li>
  <li>Verify imports by checking the tables folder in SSMS.</li>
</ol>

<!--Compare_Columns.py -->
<h3>Compare_Columns.py</h3>
<h4>Prerequisites</h4>
<p><strong>Libraries Used</strong></p>
<ul>
  <li>os</li>
  <li>pandas</li>
</ul>

<p><strong>Required Setup</strong></p>
<ul>
  <li>The files being compared must both be CSVs</li>
</ul>

<p><strong>Using the tool: Compare_Columns</strong></p>
<ol>
  <li>Run the Compare_Colums script.</li>
  <li>Input the filepath to the folder holding the first file you are comparing.</li>
  <li>Select the desired folder by index.</li>
  <li>Select the index of the dataset.</li>
  <li>Input the filepath to the folder holding the second file you are comparing.</li>
  <li>Select the desired folder by index.</li>
  <li>Select the index of the dataset.</li>
  <li>The output will start with the columns that dont match, next are any columns missing within within the first file, and the third are the columns missing in the second file/</li>
</ol>


<!--Excel_to_CSV.py -->
<h3>Excel_to_CSV.py</h3>
<h4>Prerequisites</h4>
<p><strong>Libraries Used</strong></p>
<ul>
  <li>os</li>
  <li>pandas</li>
</ul>

<p><strong>Required Setup</strong></p>
<ul>
  <li>The file getting converted to CSV must be an excel document.</li>
</ul>

<p><strong>Using the tool: Excel_to_CSV</strong></p>
<ol>
  <li>Run the Compare_Colums script.</li>
  <li>Input the filepath to your excel file.</li>
  <li>Input the linking value. This is used to link all tabs to a single value across all sheets.</li> 
  <li>Do this for all xlsx files. Input s to skip unwanted files.</li>
</ol>

