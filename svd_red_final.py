#SVD with 90% retained energy implementation
import timeit
import math
import numpy as np
from numpy import linalg
from svd_pl import svd



def rmse(matrix, final):
	error_rmse=0
	count=0
	for i in range(0,len(matrix)):
		for j in range(0,len(matrix[i])):
			error_rmse+=(matrix[i][j]-final[i][j])**2
			count+=1
	error_rmse=error_rmse/count
	error_rmse=math.sqrt(error_rmse)
	return error_rmse


def ponk_svd(mat,U,sigma,V):
	k=0
	trace=sigma.trace()
	sum_u=0
	sum_l=trace
	i=0
	while(sum_u<10*sum_l):
		sum_u=sum_u+sigma[i][i]
		sum_l=sum_l-sigma[i][i]
		k=k+1
		i=i+1
		if(i>len(sigma)-1):
			break
	print("\nPrecision on top ", k, " values.")
	while(k):
		x=len(sigma)-1
		sigma=np.delete(sigma,x,0)
		sigma=np.delete(sigma,x,1)
		U=np.delete(U,len(U[0])-1,1)
		V=np.delete(V,len(V.T[0])-1,0)
		k=k-1
	k_mat=(np.dot(U,np.dot(sigma,V)))
	for i in range(len(k_mat)):
		for j in range(len(k_mat[i])):
			k_mat[i][j]=round(k_mat[i][j],2)
	count=0.00
	match=0.00
	for i in range(0,len(mat)):
		for j in range(0,len(mat[i])):
			count=count+1
			a=int(round(mat[i][j]))
			b=int(round(k_mat[i][j]))
			if (a==b):
				match=match+1
	precision=(match*100)/count
	return precision

def srcr(mat,final):
	count=0
	sumds=0
	for i in range(0,len(mat)):
		for j in range(0,len(mat[i])):
			sumds=sumds+(mat[i][j]-final[i][j])**2
			count=count+1
	sumds=6*sumds
	den=(count**3)-count
	p=1-(sumds/den)
	return p

def process(name):
	file=open(name,"r")
	raw=file.readlines()
	ratings=[]
	for line in raw:
		irate=[]
		line=line.split("\t")
		user=int(line[0])
		irate.append(user)
		movie=int(line[1])
		irate.append(movie)
		score_rate=float(line[2])
		irate.append(score_rate)
		ratings.append(irate)
	max_movie=0
	max_user=ratings[len(ratings)-1][0]
	for rate in ratings:
		if rate[1]>max_movie:
			max_movie=rate[1]
	rating_matrix=np.zeros((max_user, max_movie))
	for rate in ratings:
		rating_matrix[rate[0]-1][rate[1]-1]=rate[2]
	
	for i in range(len(rating_matrix)):
		sum=0
		count=0
		for j in range(len(rating_matrix[i])):
			sum=sum+rating_matrix[i][j]
			count=count+1.0
		avg=sum/count
		for k in range(len(rating_matrix[i])):
			rating_matrix[i][k]=rating_matrix[i][k]-avg

	rating_matrix=rating_matrix-rating_matrix.mean(axis=1,keepdims=True)
	return rating_matrix


def svd_red(matrix):
	
	# print("Initial matrix\n")
	# print(matrix)
	
	U,sig,V=svd(matrix)

	# print("Initially U,Sig,V are :-\n")
	# print(U.shape)
	# print(sig.shape)
	# print(V.shape)

	square_eigen=0
	flag=1
	for i in range(len(sig)):
		square_eigen=square_eigen+(sig[i][i]**2)
	current=square_eigen
	while (current>(0.9*square_eigen) and flag==1):
		temp=sig[len(sig)-1][len(sig)-1]
		temp=temp**2
		sum_del=current-temp
		if(sum_del>(0.9*square_eigen)):
			current=sum_del
			x=len(sig)-1
			sig=np.delete(sig,x,0)
			sig=np.delete(sig,x,1)
			U=np.delete(U,len(U[0])-1,1)
			V=np.delete(V,len(V.T[0])-1,0)
		else:
			flag=0
	return U,sig,V	
	# print("After 90% energy retention\n")		
	# print(U.shape)
	# print(sig.shape)
	# print(V.shape)


matrix=process("ratings.txt")
start=timeit.default_timer()
U,sig,V=svd_red(matrix)
final=(np.dot(U,np.dot(sig,V)))

# for i in range(len(final)):
# 	for j in range(len(final[i])):
# 		final[i][j]=round(final[i][j],2)
		
# print("U:\n")
# print(U)
# print("sig:\n")
# print(sig)
# print("V\n:")
# print(V)
# print("\nMul of U,sig,V:")
# print(final)
print ("Time taken:\n")
stop=timeit.default_timer()
print("%s seconds" %(stop-start))
rmse_err=rmse(matrix,final)
print("Rmse error is ")
print(rmse_err)
please=ponk_svd(matrix,U,sig,V)
print(please)
answer=srcr(matrix,final)
print("spearman is",answer)