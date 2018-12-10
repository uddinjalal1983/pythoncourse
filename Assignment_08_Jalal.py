#!/bin/python3

import mysql.connector as mc
import pandas as pd
import unittest

from pandas import DataFrame
from sklearn import datasets as ds


print(mc.__version__)

connection = mc.connect(user='root', password='SQLjalal2018',
				 host='localhost', auth_plugin='mysql_native_password')

create_sql_table ='''
 
        CREATE TABLE iris_data (
			id INT NOT NULL,
			feature_sepal_length FLOAT NOT NULL,
			feature_sepal_width FLOAT NOT NULL,
			feature_petal_length FLOAT NOT NULL,
			feature_petal_width FLOAT NOT NULL,
			target_species VARCHAR(20) NOT NULL,
			target_species_id INT NOT NULL
		);

'''

class Iris(object):

	def __init__(self, creds, dbname='data602', new=True):
		self.__conn = connection  # connect to the database store
		self.__dbname = dbname

		# check if the database is new
		if new:
			pass
		else:
			self.__create()

	def __create(self):
		"""
			drop the database and create a new one
		:return:
		"""
		self.__conn.cursor().execute(create_sql_table)
		self.close()

	def close(self):
		"""
			close the database connection
		:return:

		"""
		self.__conn.cursor().close()
		print("Disconnected ")

	def load(self, truncate=False):
		"""
			loop through the iris data and inserts the data into the iris database
		:param truncate:
		:return:
		"""

		self.iris = ds.load_iris()
		self.df = pd.DataFrame(self.iris.data, columns=self.iris.feature_names)
		self.columns1 = ['feature_sepal_width','feature_sepal_width','feature_petal_length','feature_petal_width']
		self.df.columns = self.columns1
		self.custom_ids =range(len(self.df))
		self.df.insert(loc=0,column='id',value=self.custom_ids)
		self.df["target_species"] = 'setosa'
		self.df['target_id']= 0

		if truncate:
			#print("Iris data truncated ")

			# loop through the rows
			for item in self.df.columns:
				sql = "INSERT %s INTO %s ".format(self.df[item],self.__dbname)
				cursor = self.__conn.cursor()
				cursor.execute(sql)

		print("Iris data loaded ")

	def display_gt(self, n):
		"""
			displays all the rows that have an id greater than n
		:param n:
		:return:
		"""
		self.large_id = self.df.loc[self.df['id']>n]
		print(self.large_id)

	def update_observation(self, id, new_target_species, new_target_species_id):
		"""
		Update the observation with a new id to the new target species
		:param id:
		:param new_target_species:
		:param new_target_species_id:
		:return:
		"""
		self.df['target_species'] = new_target_species
		self.df['target_id'] = new_target_species_id

	def del_observations(self, rows_ids):
		"""
			deletes all the rows that are in the row ids
		:param rows_ids:
		:return:
		"""

		for item in rows_ids:
			df2 = df[df.id !=item]

	def __truncate_iris(self):

		"""
			truncate the iris data
		:return:
		"""
		self.df

	def __get_connections(self, creds):
		"""
			establish the connection
		:param creds:
		:return:
		"""
		return mc.connect(user=creds['root'], password=creds['SQLjalal2018'],
		       host='localhost', auth_plugin='mysql_native_password')

	def get_row_count(self):
		"""
			return the current row count of the iris database
		"""
		sql = "SELECT * FROM %s".format(self.__dbname)
		cursor2 = self.__conn.cursor()
		try:
			cursor2.execute(sql)
			row = 0
			results = cursor2.fetchAll()
			for result in results:
				row+= 1
		except Exception:
			pass

		return row

def get_credentials():
	# change the password
	return {'user': 'root', 'password': 'SQLjalal2018'}

def main():
	creds = get_credentials() # get the credentials
	iris = Iris(creds) # creates a new database
	iris.load() # load data from the sktlearn and pump it into iris data

	# calling the methods from the Iris class
	iris.display_gt(140) # displays all tables with row ids > 140

	# create a new database
	iris2 = Iris(creds, dbname='anotherone')
	iris2.load() # load the iris data
	iris2.del_observations([0, 1, 2]) # delete observations with equal ids

	iris2.update_observation(0, "stuff", 5)

	# close the connection to the database
	iris.close()
	iris2.close()



class TestAssignment8(unittest.TestCase):

	def test(self):
		creds = get_credentials()
		db1 = Iris(creds)
		self.assertEqual(db1.get_row_count(), 0)
		db1.load()
		self.assertEqual(db1.get_row_count(), 150)
		db1.load()
		self.assertEqual(db1.get_row_count(), 300)
		db2 = Iris(creds, dbname='data602x')
		self.assertEqual(db1.get_row_count(), 0)
		db2.load()
		self.assertEqual(db1.get_row_count(), 150)
		db1.load(truncate=True)
		self.assertEqual(db1.get_row_count(), 150)
		db1.display_gt(148)
		db2.display_gt(148)
		db1.del_observations([0, 1, 2, 3, 4, 5])
		self.assertEqual(db1.get_row_count(), 144)
		self.assertEqual(db2.get_row_count(), 150)


if __name__ == '__main__':
	unittest.main()
