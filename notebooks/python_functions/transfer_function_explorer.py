def laplace_calc(x,y,system):
    
    tf = system.to_tf()  
    
    num=np.array(np.zeros([len(x),len(y)]))
    for exponent, coef in enumerate(tf.num[::-1]):
        num=np.add(num,np.multiply((x+1j*y)**exponent, coef))
        
    den=np.array(np.zeros([len(x),len(y)]))
    for exponent, coef in enumerate(tf.den[::-1]):
        den=np.add(den,np.multiply((x+1j*y)**exponent, coef))

    
    return np.divide(num,den)
    
    
def laplace_plot(system, xlim = [-10,10],
                 ylim = [-10,10],
                 zlim = [0,5],
                 surface = True,
                 plane = True,
                 line = True,
                 res= 1000):
    
    x = np.linspace(xlim[0], xlim[1], res)
    y = np.linspace(ylim[0], ylim[1], res)

    yl=np.logspace(ylim[0],ylim[1],res)

    xx, yy = np.meshgrid(x, y)
    xxl, yyl = np.meshgrid(x, yl)

    l=laplace_calc(xx,yy,system)
    ll=laplace_calc(np.zeros(res),y,system)


                 
    z=np.abs(l)         
    #z=np.log10(np.abs(l))
    z=np.clip(z,zlim[0],zlim[1])   
    
    zline=np.abs(ll)
    #zline=np.log10(np.abs(ll))
    zline=np.clip(zline,zlim[0],zlim[1])       
                 
                 
    p=np.angle(l,deg=True)

    colormap = cm.viridis
    znorm = (p/10)+0.5
    #znorm /= znorm.ptp()
    #znorm.min(), znorm.max()
    color = colormap(znorm)

    
    if surface: 
        m = ipv.plot_mesh(xx, yy, z, wireframe=False,color=color[...,0:3])
    if plane:
        ipv.plot_trisurf(0,[ylim[0], ylim[0], ylim[1], ylim[1]],[zlim[0], zlim[1], zlim[0], zlim[1]],
           triangles=[[0, 2, 3], [0, 3, 1]])
    if line:
        ipv.plot(np.zeros(res),y,zline,color='black')



    ipv.squarelim()
    
    ipv.xlim(xlim[0],xlim[1])
    ipv.ylim(ylim[0],ylim[1])
    ipv.zlim(zlim[0],zlim[1])