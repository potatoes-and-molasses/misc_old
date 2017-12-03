package dec;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class decrypt {

	public static void main(String[] args) {
		
		
		
		byte [] iv = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
		try{
			IvParameterSpec spec = new IvParameterSpec(iv,0,iv.length);
			byte [] fin = CryptoBase64.decode("b64pass".getBytes("UTF-8"));
			String key =  "com.esri."+q;
			
			byte [] keyb = key.getBytes("UTF-8");
			byte [] another = new byte[16];
			
			System.arraycopy(keyb,0,another,0,16);
			SecretKeySpec realkey = new SecretKeySpec(another,"AES");
			Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
			
			cipher.init(2,realkey,spec);
			
			byte [] good = cipher.doFinal(fin);
			
			int valid = 1;
			String hurray = new String(good,"UTF8");
			System.out.println(hurray);
			
			
		}
		catch (Exception e){
		}
		
		}
		
		
	}

