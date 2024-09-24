//DEPS org.springframework:spring-context:6.1.13

import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.*;

/**
 * The main class that runs the Spring application using JBang.
 */
public class HelloWorldSpringDI {

    /**
     * The entry point of the application.
     *
     * @param args Command-line arguments (not used).
     */
    public static void main(String... args) {
        ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
        MessageRenderer mr = ctx.getBean(MessageRenderer.class);
        mr.render();
    }
}

/**
 * Spring configuration class that defines beans for the application.
 */
@Configuration
class AppConfig {

    /**
     * Creates a {@link MessageProvider} bean.
     *
     * @return A new instance of {@link HelloWorldMessageProvider}.
     */
    @Bean
    public MessageProvider provider() {
        return new HelloWorldMessageProvider();
    }

    /**
     * Creates a {@link MessageRenderer} bean and injects the {@link MessageProvider}.
     *
     * @return A new instance of {@link StandardOutMessageRenderer}.
     */
    @Bean
    public MessageRenderer renderer() {
        StandardOutMessageRenderer renderer = new StandardOutMessageRenderer();
        renderer.setMessageProvider(provider());
        return renderer;
    }
}

/**
 * Interface for rendering messages.
 */
interface MessageRenderer {

    /**
     * Renders the message to the appropriate output.
     */
    void render();

    /**
     * Sets the message provider.
     *
     * @param provider The {@link MessageProvider} to use.
     */
    void setMessageProvider(MessageProvider provider);

    /**
     * Retrieves the current message provider.
     *
     * @return The current {@link MessageProvider}.
     */
    MessageProvider getMessageProvider();
}

/**
 * Interface for providing messages.
 */
interface MessageProvider {

    /**
     * Gets the message to be rendered.
     *
     * @return The message as a {@link String}.
     */
    String getMessage();
}

/**
 * Implementation of {@link MessageProvider} that returns a "Hello World" message.
 */
class HelloWorldMessageProvider implements MessageProvider {

    /**
     * Constructs a new {@code HelloWorldMessageProvider} and outputs a creation message.
     */
    public HelloWorldMessageProvider(){
        System.out.println(" --> HelloWorldMessageProvider: constructor called");
    }

    /**
     * Returns the "Hello World!" message.
     *
     * @return A {@link String} containing "Hello World!".
     */
    @Override
    public String getMessage() {
        return "Hello World!";
    }
}

/**
 * Implementation of {@link MessageRenderer} that outputs messages to the standard output.
 */
class StandardOutMessageRenderer implements MessageRenderer {

    private MessageProvider messageProvider;

    /**
     * Constructs a new {@code StandardOutMessageRenderer} and outputs a creation message.
     */
    public StandardOutMessageRenderer(){
        System.out.println(" --> StandardOutMessageRenderer: constructor called");
    }

    /**
     * Renders the message provided by the {@link MessageProvider}.
     *
     * @throws RuntimeException if the {@code messageProvider} is not set.
     */
    @Override
    public void render() {
        if (messageProvider == null) {
            throw new RuntimeException(
                "You must set the property messageProvider of class: " + StandardOutMessageRenderer.class.getName());
        }
        System.out.println(messageProvider.getMessage());
    }

    /**
     * Sets the {@link MessageProvider}.
     *
     * @param provider The {@link MessageProvider} to set.
     */
    @Override
    public void setMessageProvider(MessageProvider provider) {
        System.out.println(" --> StandardOutMessageRenderer: setting the provider");
        this.messageProvider = provider;
    }

    /**
     * Gets the current {@link MessageProvider}.
     *
     * @return The current {@link MessageProvider}.
     */
    @Override
    public MessageProvider getMessageProvider() {
        return this.messageProvider;
    }
}
