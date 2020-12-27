#------------------------------------ Libraries---------------------------------------------------------------------------------
import networkx as nx 
import matplotlib.pyplot as plt
from collections import Counter 
from networkx.algorithms.community import greedy_modularity_communities



#-------------------------------1. generating network---------------------------------------------------------------------------
Size=115
Graph = nx.barabasi_albert_graph(Size,8) #Generate a scale-free network
nx.draw(Graph, with_labels=True) 



#-------------------------------2. drawing degree distribution----------------------------------------------------------------
def draw_Degree_Distribution(Graph,plot_name,size_value):
    derece_dizisi = sorted([i for j, i in Graph.degree()], reverse=True)  
    derece_sayisi = Counter(derece_dizisi)
    derece, sayac = zip(*(derece_sayisi.items()))
    pk =[]
    for i in sayac:
        pk.append(i/size_value)
    sekil, eksen_x = plt.subplots()
    plt.bar(derece, pk, width=0.88, color='green')
    plt.title(plot_name+" Degree Distribution")
    plt.ylabel("P(k)     (Probability)")
    plt.xlabel("k (Degree)")
    temp_list=[]
    for i in derece_dizisi :
        temp_list.append(i+0.4)
    eksen_x.set_xticks(temp_list)    
    eksen_x.set_xticklabels(derece_dizisi)
    

draw_Degree_Distribution(Graph,"Network",Size)    
plt.show()


#-------------------------------3.Find all communities in the network---------------------------------------------------------
communities = sorted(greedy_modularity_communities(Graph), key=len, reverse=True)
#print(communities)

#top_level_communities = next(comp)
#next_level_communities = next(comp)
#sorted(map(sorted, next_level_communities))
#print(len(next_level_communities))



#-------------------------------4.Print the number of communities---------------------------------------------------------------
print("----------------------------------------------------------------------------------------")
print("Number of comminities : ",len(communities))

print("----------------------------------------------------------------------------------------")
#-------------------------------5.Give a name each community.Use names as community1, community2,… ----------------------------
dic={}   #for each community , have subnet name. I stored all of them in a dictionary 
name="community"
for sayi in range(0,len(communities)):
    dic[name+str(sayi+1)]=list(communities[sayi])

#name subnet control for each community
#print("-----------Control all communities-----------")
#for com in dic:
#    print(com,"   ==>    ",dic[com])
#    print("    ")
#   print("    ")





#------------------------------6.Print the size and the node labels in each community.-------------------------------------
class ColorsForPrint:
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"                           #10 space
print(ColorsForPrint.BOLD + "Community Name          Community Size          Nodes In The Community" + ColorsForPrint.END)

for com in dic :
    print(com,"             ",len(dic[com]),"              ",end =" ")  # python 3 ve üstü icin newline sız print etme
    print(*dic[com],sep=',')
    print("     ")
    print("     ")





#---------------------------7.Draw the network by coloring each node with different color for different communities.------------

def Kenarlar_icin_commity_durumu(Grap):
#Her Community nodelarının birbiriyle olan kenar durumlarını bulup, ilgili topluluğun üzerine bu veriler ekledim.
        for i, j, in Grap.edges:
            if Grap.nodes[j]['Group'] ==  Grap.nodes[i]['Group'] : #her topluluğun nodelarının birbiriyle olan iç kenardurumu!
                Grap.edges[i, j]['Group'] = Grap.nodes[i]['Group'] #durumlar sağlanınca kenar için gerekli atama yaptım
            else:
                Grap.edges[i, j]['Group'] = 0 # ilgili community ile alakasız olan kenar durumu

#düğüm topluluğunu ayarladım,her topluğun üye nodelarınının aynı rengi alması için gerekli function olusturdum.
def Community_Of_Nodes(Grap, communities):
        for i, j in enumerate(communities):    #Node özelliklerini, daha önce bulduğum communities üzerinden gerçekleştirdim.
            for m in j:
                #Buradaki 'Group',fonk için yaptigim community isimlerine karşılık gelen
                #ve her community için onları temsil  temp variable gibi
                #Örneğin Community_Of_Nodes çağırdığımda ilk community ismi olan 'community1' e karsılık,
                #'Group' community name ni alıyor.
                #fonk'un diğer communities içinde aynı şeyi yapmakta 
                Grap.nodes[m]['Group'] = i + 1 #Communitynin dışındaki kenarlar için,  kaydetmek için 0,
                                                #eklemek için 1 ekledim
#Her commnity nin node üyelerini aynı renge boyamak için gerekli renk fonksiyonu!
def Community_ici_renkleri(al, offset_r = 1, offset_g = 1, offset_b = 1):
        min=0.1
        max=0.9
        n_sat= 16
        red = ((max - min)* (((offset_r+al)* 3) % n_sat) /(n_sat - 1)+min)
        green =((max - min)* (((offset_g+al)* 5) % n_sat) /(n_sat - 1)+min)
        blue =((max - min)* (((offset_b+al)* 7) % n_sat) /(n_sat - 1)+min)
        return (red,green,blue)  

# Her community içi ve communityler arası,nodes ve edges birbiriyle ilişki durumu  inceledim
Community_Of_Nodes(Graph, communities)
Kenarlar_icin_commity_durumu(Graph)
Color_of_Node =[]
#Topluluk içi renklendirme
for i in Graph.nodes:
      Color_of_Node.append(Community_ici_renkleri(Graph.nodes[i]['Group']))
# topluluklar arası ve içi kenar durumları
topluluklar_arasi_kenarlar =[]
for i,j in Graph.edges:
     if Graph.edges[i, j]['Group'] == 0:
            topluluklar_arasi_kenarlar.append((i,j))  # her i,j arası kenarlar, topluluklar arası kenarlar 
topluluk_ici_kenarlar=[]
for i,j in Graph.edges:
    if Graph.edges[i, j]['Group'] > 0:
            topluluk_ici_kenarlar.append((i,j))            
ic_kenar_renk_durumu = []
for i in topluluk_ici_kenarlar:
     ic_kenar_renk_durumu.append('black')

#ismags = nx.isomorphism.ISMAGS(Graph, Graph)   
#isomorphisms = list(ismags.isomorphisms_iter(symmetry=True))
positon = nx.spring_layout(Graph)
plt.rcParams.update({'figure.figsize': (14,9)})
#Topluluklar arası node ve kenarlar durumu icin
nx.draw_networkx(
   Graph,
   pos=positon,
   node_size=0,
   edgelist=topluluklar_arasi_kenarlar,
   edge_color="silver")
#Her Topluluk içi node ve kenarlar durumu icin
nx.draw_networkx(
   Graph,
   pos=positon,
   node_color=Color_of_Node,
   edgelist=topluluk_ici_kenarlar,
   edge_color=ic_kenar_renk_durumu)
#Her renk bir topluluğu temsil ediyor ve bu topluluk listesi 6. soru kısmında node bilgileriyle birlikte mevcut





#---------------------------------------8.Assign each community to a new network.-----------------------------------------------
sub_nests={}
subnets_sizes=[]  #Her subnet için
name_s="sub_network"
i=0
for com in dic:  #for sayi in range(0,len(communities)):    Her community yi bir subnete atadım 
    i=i+1                                                  #Her subnet degree dist. olluşturmak icin node ve edge durumlarıyla 
    subnets_sizes.append(len(dic[com]))
    sub_nests[name_s+str(i)]=nx.Graph()                    #Hazır hale geldi,bu verileri 'sub_nests' adında dictionary de 
    (sub_nests[name_s+str(i)]).add_nodes_from(dic[com])    #tuttum,Assign işlemini bitirmiş oldum.
    temp = []
    for j in dic[com]:
        for k in topluluk_ici_kenarlar:
            if j == k[0]:
                temp.append(k)
    
    (sub_nests[name_s+str(i)]).add_edges_from(temp)
        
   

#------------------------9. Draw the degree distribution of each sub-networks (communities).------------------------------------
i=-1
for sub in sub_nests:
    i=i+1
    draw_Degree_Distribution(sub_nests[sub],sub,subnets_sizes[i])   #Her subnet için degree distrubitionın bastırdım.

#For Scale-free Network,Preferential attachment is a probabilistic mechanism: 
#A new node is free to connect to any node in the network, whether it is a hub or has a single link.
# But if we give an important example,if a new node has a choice between a degree-two and a degree-four node,
#it is twice as likely that it connects to the degree-four node.(Öncelikli tercihi hublaşmanın yoğun olduğu nodeları seçeçektir.)
#The presence of hubs will give the degree distribution a long tail,
#indicating the presence of nodes with a much higher degree than most other nodes.
#Her community'i bir subnet olarak ayırma yaptığımızda, 
#ilgili subnet'in size,node ve kenar bilgilerini kullanarak(bu bilgiler empty graph'a yerleştirilmekte olan her subnet icin 8. kısımda yapılmakta),  
#çıkardiğimiz degree distributionlar'a bakarak subnetlerde de başlangiçtaki scale-free network mantiğina paralel olarak,
#benzer durum söz konusudur.Sonuç olarak,subnetler de bir Scale-Free Network'tur.