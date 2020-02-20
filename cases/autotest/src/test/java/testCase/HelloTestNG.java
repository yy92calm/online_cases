package testCase;

import org.testng.Assert;
import org.testng.annotations.Test;

public class HelloTestNG {

    @Test(groups = "main")
    public void success_test_01()
    {
        System.out.println("This is main test01!");
        Assert.assertNull(null);
    }

    @Test(groups = "other")
    public void success_test_02()
    {
        System.out.println("This is main test01!");
        int i = 2;
        Assert.assertEquals(1,i);
    }
}
