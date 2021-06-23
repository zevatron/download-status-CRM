import csv

grouped = {'MG':[]}

with open('3MEDICOS_CRM.csv',newline='') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';')
	for row in reader:
		crm = row['NUM_CONSELHO']
		uf = row['UF_CONSELHO']
		if uf not in grouped.keys() :
			grouped[uf] = [crm]
		else:
			grouped[uf].append(crm)

print(grouped)
