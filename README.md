# Joint-Ultimatum-Game
This code was created for a master's thesis project. It provides a PsychoPy code for a Joint Ultimatum Game where 2 players act as responders against a virtual confederate implemented in the code.

**** Instructions for using the code for the project "Joint decision-making and punishment in the repeated Ultimatum Game ****

PC requirements for running the code: 

- At least 2 Windows PCs with Python 3.8.10+ installed
- The PCs have to be in the same Network and Working Group
- OR they have to be connected together via a LAN-cable
- The network settings on the PCs have to allow file sharing - at least PC2 has to be able to access PC1s files
- If WhatsApp should be opened automatically - Python needs permission to open WhatsApp - google for instructions
- Packages in the first rows of the code installed
- You can also use the PsychoPy Standalone version (Psychopy 3) 

How the codes work in general: 

- JD_P1.py relates to Player1 & JD_P2.py to Player2
- Each code runs a separate Ultimatum Game against an algorithm that is built in the code itself
- The codes write into files to communicate
- The folder "Files" contains 12 .txt and 2 .py files
- In ALL the .py files change the path variables to the correct path of PC1 where the codes and files are stored
- DONT change path_variable names
- Put JD_P1.py and HEXACO_P1.py and the folder "Files" in the same folder on PC1
- Put JD_P2.py and HEXACO_P2.py in the same folder on PC2
- On each of the PCs CREATE AN EXCEL called JD_P1.xlsx and hexaco_P1.xlsx as well as JD_P2.xlsx hexaco_P2.xlsx respectively for the data collection


File functions:

- ready.txt and ready2.txt serve as communicators whether both players are ready to synchronize the games 
- In the Joint Phase Players play together and always receive the same offers
- P1Response.txt and P2Response.txt serve for the joint phase, so codes know what the other player decided 
- The joint offer will be written into Offer.txt by JD_P1.py so JD_P2.py knows what the offer is 
- part_file.txt and part_file2.txt serves for keeping track of the participant number

- Run 0_Clear files.py to clear all files except for part_file.txt and part_file2.txt 
 (should all be clear after a whole experimental run automatically but in case you had to abort or just to be sure)
- Run 1_Clear files.py to clear ALL FILES including the participant files - then it will start from participant1 again

- The codes write their data into the excel files and will create a new sheet for every run (i.e., for each participant) 


Running the experiment: 

- Once everything is setup, just run both codes on the PCs and the game can start
- For the Joint Phase, there are two functions in the code openWhatsapp() and closeWhatsapp()
- If these don't work it may be because of Microsoft App restrictions --> if these can't be circumvented:
  Just comment the functions out and open and close Whatsapp manually

Questionnaires after the experiment: 

- HEXACO_P1.py and HEXACO_P2.py contain code for personality questionnaires and some following post-experiment questionnaires
- They will be automatically run by the code as well and don't require any changes
- The questionnaire data will be saved on the excel files called hexaco_P1.xlsx and hexaco_P2.xlsx respectively for each participant once the excel file is created

If you want to change experimental conditions In JD_P1.py and JD_P2.py relatively close to the top of the code you can change:
 
pool_money = 10 #for changing how many points are in the pool
num_trials = 20 #for changing the number of rounds in the joint phase
base_trials = 20 #for changing the number of rounds in the individual phase1 and individual phase2 

discussTimer = 90 #for changing the discussion time (in seconds)
decisionTimer = 10 #for changing time limit for decisions (in seconds) 

PLEASE DONT CHANGE ANYTHING ELSE IN THE CODES
