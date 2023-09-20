import sys
import json
import random
import qrcode
import hashlib
import datetime

from send_email import send_email


VERIFICATION_URL = "http://127.0.0.1:5000/verify/"

class Login:

	MANF = ""
	LOGGEDIN = False
	MANUFACTURERS = {
		"Mitesh": "password123",
		"Ahefaz": "hello123",
		"rushi": "qwerty",
		"ADMIN": "qwerty"
	}

	def main(self):
		loginid = input("Enter your login id:\t")
		password = input("Enter your password:\t")

		if loginid in self.MANUFACTURERS.keys():
			if self.MANUFACTURERS[loginid] == password:
				self.LOGGEDIN = True
				self.MANF = loginid

	def isLoggedIn(self):
		if self.LOGGEDIN:
			print("\nWelcome to the blockchain world\n")
		else:
			sys.exit("Please login to experience the blockchain world")

	def getManf(self):
		return self.MANF


class BlockChain:

	def __init__(self):
		self.s_department = ""
		self.s_name = ""
		self.s_batch = ""
		self.dob_date = ""
		self.pass_date = ""
		self.s_id = ""
		self.s_cgpa = ""
		self.s_grade = ""
		self.s_type = ""


	def actions(self):
		choice = input("Enter 1 to ADD item or 2 to Verify BlockChain\n")

		if choice == "1":
			self.s_department = input("DEPARTMENT : ")
			self.s_name = input("NAME : ")
			self.s_batch = input("BATCH YEAR : ")
			self.dob_date = input("DATE OF BIRTH : ")
			# self.pass_date = input("Enter certificate passing date:\n")
			self.s_id = input("REGISTRATION NO. : ")
			self.s_cgpa = input("CGPA : ")
			self.s_grade = input("GRADE : ")
			self.s_type = input("COLLEGE : ")
			self.newProduct()

		elif choice == "2":
			if self.isBlockchainValid():
				sys.exit("BlockChain is valid")
			else:
				sys.exit("BlockChain is invalid")

		else:
			sys.exit("Logged out successfully")


	def newProduct(self):
		data = {
			"Department": self.s_department,
			"PName": self.s_name,
			"PBatch": self.s_batch,
			"PdobDate": self.dob_date,
			"PpassDate": self.pass_date,
			"PId": self.s_id,
			"Pcgpa": self.s_cgpa,
			"Pgrade": self.s_grade,
			"PType": self.s_type,
		}

		proHash = hashlib.sha256(str(data).encode()).hexdigest()
		print(proHash)
		data["hash"] = proHash

		self.createBlock(data)

		imgName  = self.imgNameFormatting()
		self.createQR(proHash, imgName)

	def addProduct(
		self,
		s_department,
		s_name,
		s_batch,
		dob_date,
		pass_date,
		s_id,
		s_cgpa,
		s_grade,
		s_type
	):
		self.s_name = s_name
		data = {
			"Department": s_department,
			"PName": s_name,
			"PBatch": s_batch,
			"PdobDate": dob_date,
			"PpassDate": pass_date,
			"PId": s_id,
			"Pcgpa": s_cgpa,
			"Pgrade": s_grade,
			"PType": s_type,
		}

		proHash = hashlib.sha256(str(data).encode()).hexdigest()
		print(proHash)
		data["hash"] = proHash

		# x = mycol.insert_one(data)
		grade = data["Pgrade"]
		subject = 'B-12'
		body = f'Dear Student,\n\n Your certificate has generated successfully with Certificate Unique Number {proHash} \n\nSincerely,\nB12 Final year project '
		send_email(grade, subject, body)
		self.createBlock(data)

		imgName = self.imgNameFormatting()
		self.createQR(proHash, imgName)


	def createBlock(self, data):

		if self.isBlockchainValid():
			blocks = []
			for block in open('./NODES/N1/blockchain.json', 'r'):
				blocks.append(block)
			print(blocks[-1], "jsdata===========")

			preBlock = json.loads(blocks[-1])

			index = preBlock["index"] + 1
			preHash = hashlib.sha256(str(preBlock).encode()).hexdigest()

		transaction = {
			'index': index,
			'proof': random.randint(1, 1000),
			'previous_hash': preHash,
			# 'hash': proHash,
			'timestamp': str(datetime.datetime.now()),
			'data': str(data),
		}

		with open("./NODES/N1/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))
		with open("./NODES/N2/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))
		with open("./NODES/N3/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))
		with open("./NODES/N4/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))

		# currHash = hashlib.sha256(str(transaction).encode()).hexdigest()
		# imgName  = self.imgNameFormatting()

		# self.createQR(currHash, imgName)
		return


	def createQR(self, hashc, imgName):
		img = qrcode.make(VERIFICATION_URL + hashc)
		img.save("./QRcodes/" + imgName)

		# sys.exit("certificate added successfully")
		return


	def imgNameFormatting(self):
		dt = str(self.s_grade)
		return self.s_name + self.s_grade + self.s_id + "_" + dt + ".png"


	def isBlockchainValid(self):
		with open("./NODES/N1/blockchain.json", "r") as file:
			n1_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n1_hash)
		with open("./NODES/N2/blockchain.json", "r") as file:
			n2_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n2_hash)
		with open("./NODES/N3/blockchain.json", "r") as file:
			n3_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n3_hash)
		with open("./NODES/N4/blockchain.json", "r") as file:
			n4_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n4_hash)

		if n1_hash == n2_hash == n3_hash == n4_hash:
			return True
		else:
			return False


if __name__ == "__main__":
	lof = Login()
	lof.main()
	lof.isLoggedIn()

	LOGGEDINUSER = lof.getManf()

	bc = BlockChain()
	bc.actions()