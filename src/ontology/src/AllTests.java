import org.junit.runner.RunWith;
import org.junit.runners.Suite;
import org.junit.runners.Suite.SuiteClasses;

@RunWith(Suite.class)
@SuiteClasses({TestSparqlQuerier.class, TestSparqlQueryConstructor.class})
public class AllTests {

}
