import urllib.request, os
UA={'User-Agent':'UfologyBookBuild/1.0 (contact: book build)'}
files={
 'uf_mj12_hillenkoetter.jpg':'https://upload.wikimedia.org/wikipedia/commons/9/9e/Roscoe_H._Hillenkoetter_%281957%29.jpg',
 'uf_mj12_twining.jpg':'https://upload.wikimedia.org/wikipedia/commons/1/1f/Gen_Nathan_F._Twining%2C_black_and_white_portrait.jpg',
 'uf_mj12_vandenberg.jpg':'https://upload.wikimedia.org/wikipedia/commons/8/8d/Hoyt_S_Vandenberg.jpg',
 'uf_mj12_montague.jpg':'https://upload.wikimedia.org/wikipedia/commons/6/6c/Robert_Miller_Montague.jpg',
 'uf_mj12_souers.jpg':'https://upload.wikimedia.org/wikipedia/commons/9/93/Sidney_W._Souers.jpg',
 'uf_mj12_forrestal.jpg':'https://upload.wikimedia.org/wikipedia/commons/5/5c/James_Forrestal_-_SecOfDef.jpg',
 'uf_mj12_gray.jpg':'https://upload.wikimedia.org/wikipedia/commons/e/e0/Gordon_Gray_-_Project_Gutenberg_etext_20587.jpg',
 'uf_mj12_bush.jpg':'https://upload.wikimedia.org/wikipedia/commons/1/1e/Vannevar_Bush%2C_1938%2C_Harris_%26_Ewing_%28cropped%29.jpg',
 'uf_mj12_bronk.jpg':'https://upload.wikimedia.org/wikipedia/commons/7/7b/Detlev_Wulf_Bronk.jpg',
 'uf_mj12_hunsaker.jpg':'https://upload.wikimedia.org/wikipedia/commons/3/33/Jerome_Clarke_Hunsaker_%28cropped%29.jpg',
 'uf_mj12_menzel.jpg':'https://upload.wikimedia.org/wikipedia/commons/5/54/Donald_Howard_Menzel_Portrait.jpg',
 'uf_mj12_berkner.jpg':'https://upload.wikimedia.org/wikipedia/commons/b/b1/Lloyd_Berkner.jpg',
}
for n,u in files.items():
    try:
        d=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=120).read()
        open('temp_mj12/'+n,'wb').write(d)
        print('OK  %-30s %8d' % (n,len(d)))
    except Exception as e:
        print('FAIL',n,e)
