![](Pasted%20image%2020260824175843.png)
# URLDNS Gadget链（JDK原生反序列化DNS探测链）

完整调用顺序：
`HashMap.readObject()` → `HashMap.putVal()` → `HashMap.hash()` → `URL.hashCode()` → `URLStreamHandler.hashCode()` → `URLStreamHandler.getHostAddress()` → `InetAddress.getByName()`

> 说明：`putVal()` 是**反序列化流程内部调用**，不是业务代码`map.put()`；业务put只是构造payload时用，不在反序列化gadget链本身。

## 1. HashMap.readObject()
```java
private void readObject(java.io.ObjectInputStream s) throws IOException, ClassNotFoundException {
    s.defaultReadObject();
    // 读取容量、负载因子
    int mappings = s.readInt();
    // 循环读出key、value，调用putVal完成重建
    for (int i = 0; i < mappings; i++) {
        K key = (K) s.readObject();
        V value = (V) s.readObject();
        putVal(hash(key), key, value, false, false);
    }
}
```

- 作用：HashMap自定义反序列化方法，反序列化重建map，读取每一对key‑value，调用`putVal`；**入口点**。
- key可控，这里key是`URL`对象。

## 2. HashMap.putVal()
```java
final V putVal(int hash, K key, V value, boolean onlyIfAbsent, boolean evict) {
    // 哈希表插入逻辑，第一个参数就是hash(key)算出来的哈希值
    Node<K,V>[] tab; Node<K,V> p; int n, i;
    if ((tab = table) == null || (n = tab.length) == 0)
        n = (tab = resize()).length;
    if ((p = tab[i = (n - 1) & hash]) == null)
        tab[i] = newNode(hash, key, value, null);
    else {
        // 链表/红黑树处理
    }
}
```

- 接收上游`hash(key)`的返回值；**本身不触发漏洞，但强制调用hash()**。

## 3. HashMap.hash()
```java
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

- 核心：调用`key.hashCode()`；key是URL，于是跳转到`URL.hashCode()`。
- 逻辑：把key的hashCode高16位异或低16位，打散哈希，减少碰撞。

## 4. URL.hashCode()
```java
public synchronized int hashCode() {
    if (hashCode != -1) { // 缓存！默认值是-1
        return hashCode;
    }
    hashCode = handler.hashCode(this); // handler:URLStreamHandler实例
    return hashCode;
}
```
- 关键点：字段`hashCode`默认`‑1`；**如果不等于‑1直接返回缓存，不会继续往下走**。
- payload构造时必须反射把`url.hashCode`设置回`‑1`，反序列化时才会执行`handler.hashCode(this)`，否则DNS不会触发。
- `handler`是`transient`，序列化不会保存，反序列化会重新生成handler实例。

## 5. URLStreamHandler.hashCode(URL u)
```java
protected int hashCode(URL u) {
    int h = 0;
    String protocol = u.getProtocol();
    if (protocol != null)
        h += protocol.hashCode();

    InetAddress addr = getHostAddress(u); // 关键调用！

    if (addr != null) {
        h += addr.hashCode();
    } else {
        String host = u.getHost();
        if (host != null)
            h += host.toLowerCase().hashCode();
    }
    // ...拼接file、port、ref等部分hash
    return h;
}
```

- 调用`getHostAddress(u)`，进入DNS解析逻辑。

## 6. URLStreamHandler.getHostAddress(URL u)
```java
protected synchronized InetAddress getHostAddress(URL u) {
    if (u.hostAddress != null)
        return u.hostAddress;
    String host = u.getHost();
    if (host == null || host.equals("")) {
        return null;
    } else {
        try {
            u.hostAddress = InetAddress.getByName(host); // 调用DNS解析
        } catch (UnknownHostException ex) {
            return null;
        } catch (SecurityException se) {
            return null;
        }
        return u.hostAddress;
    }
}
```

- 拿到url的host域名，调用`InetAddress.getByName(host)`，发起DNS查询请求。

## 7. InetAddress.getByName()
```java
public static InetAddress getByName(String host) throws UnknownHostException {
    return InetAddress.getAllByName(host)[0];
}
```

- JDK原生DNS解析方法，向DNS服务器发送域名解析请求；**gadget链终点**。
- 无RCE，仅DNS请求；用于探测目标是否执行了反序列化。

---

# Payload构造要点（为什么要反射修改hashCode）

1. 代码`map.put(url,xxx)`的时候，会完整走一遍整条链，**序列化阶段就会触发DNS**，这是不想要的。
2. 解决：
   - put前反射设置`url.hashCode = 非‑1`，put阶段直接返回缓存，不触发DNS；
   - put完成后，反射重置`url.hashCode = -1`；
   - 序列化HashMap；目标反序列化时，`readObject`重新走链，`hashCode==‑1`，触发DNS查询。
## 特点
1. **纯JDK原生，不需要第三方依赖**，所有JDK版本都存在；
2. 只能DNS探测，不能命令执行；
3. ysoserial `URLDNS` payload就是这条链。
