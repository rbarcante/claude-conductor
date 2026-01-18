/**
 * USE: When implementing dependency injection patterns with Spring or Jakarta EE
 * REQUIRES: Java 17+, Spring Boot 3.x or Jakarta EE 10+
 * PATTERN: Configuration, Error Handling
 */

import java.util.Objects;

// ============================================================================
// PATTERN 1: Constructor Injection (Recommended)
// ============================================================================

// CUSTOMIZE: Your service class with constructor injection
// @Service // Spring
// @ApplicationScoped // Jakarta CDI
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
    private final UserMapper userMapper;

    // Constructor injection - preferred approach
    // Spring: @Autowired is optional for single constructor
    // Jakarta CDI: @Inject required
    public UserService(
            UserRepository userRepository,
            EmailService emailService,
            UserMapper userMapper) {
        this.userRepository = Objects.requireNonNull(userRepository, "userRepository");
        this.emailService = Objects.requireNonNull(emailService, "emailService");
        this.userMapper = Objects.requireNonNull(userMapper, "userMapper");
    }

    public UserDto createUser(CreateUserRequest request) {
        var user = userMapper.toEntity(request);
        var savedUser = userRepository.save(user);
        emailService.sendWelcomeEmail(savedUser.getEmail());
        return userMapper.toDto(savedUser);
    }
}

// ============================================================================
// PATTERN 2: Configuration Classes
// ============================================================================

// CUSTOMIZE: Spring configuration class
// @Configuration
public class AppConfig {

    // @Bean
    public UserMapper userMapper() {
        return new UserMapperImpl();
    }

    // @Bean
    // @Profile("!test") // Exclude from test profile
    public EmailService emailService(EmailConfig config) {
        return new SmtpEmailService(config);
    }

    // @Bean
    // @ConditionalOnProperty(name = "feature.caching.enabled", havingValue = "true")
    public CacheManager cacheManager() {
        return new CaffeineCacheManager();
    }
}

// CUSTOMIZE: Configuration properties class
// @ConfigurationProperties(prefix = "app.email")
// @Validated
public record EmailConfig(
    // @NotBlank
    String host,
    // @Min(1) @Max(65535)
    int port,
    // @NotBlank
    String username,
    String password,
    boolean sslEnabled
) {
    public EmailConfig {
        Objects.requireNonNull(host, "host cannot be null");
        Objects.requireNonNull(username, "username cannot be null");
        if (port < 1 || port > 65535) {
            throw new IllegalArgumentException("port must be between 1 and 65535");
        }
    }
}

// ============================================================================
// PATTERN 3: Interface-Based Injection with Multiple Implementations
// ============================================================================

// Define interface
public interface NotificationService {
    void send(String recipient, String message);
}

// Implementation 1
// @Service
// @Primary // Default implementation
public class EmailNotificationService implements NotificationService {
    private final EmailService emailService;

    public EmailNotificationService(EmailService emailService) {
        this.emailService = Objects.requireNonNull(emailService, "emailService");
    }

    @Override
    public void send(String recipient, String message) {
        emailService.sendEmail(recipient, "Notification", message);
    }
}

// Implementation 2
// @Service("smsNotification")
public class SmsNotificationService implements NotificationService {
    private final SmsGateway smsGateway;

    public SmsNotificationService(SmsGateway smsGateway) {
        this.smsGateway = Objects.requireNonNull(smsGateway, "smsGateway");
    }

    @Override
    public void send(String recipient, String message) {
        smsGateway.sendSms(recipient, message);
    }
}

// Using qualifier to select implementation
// @Service
public class AlertService {
    private final NotificationService primaryNotification;
    private final NotificationService smsNotification;

    public AlertService(
            // @Primary automatically selected, or use @Qualifier
            NotificationService primaryNotification,
            // @Qualifier("smsNotification")
            NotificationService smsNotification) {
        this.primaryNotification = primaryNotification;
        this.smsNotification = smsNotification;
    }

    public void sendCriticalAlert(String recipient, String message) {
        primaryNotification.send(recipient, message);
        smsNotification.send(recipient, message);
    }
}

// ============================================================================
// PATTERN 4: Factory Pattern with DI
// ============================================================================

// Factory interface
public interface PaymentProcessorFactory {
    PaymentProcessor create(PaymentMethod method);
}

// @Component
public class PaymentProcessorFactoryImpl implements PaymentProcessorFactory {
    private final CreditCardProcessor creditCardProcessor;
    private final PayPalProcessor payPalProcessor;
    private final BankTransferProcessor bankTransferProcessor;

    public PaymentProcessorFactoryImpl(
            CreditCardProcessor creditCardProcessor,
            PayPalProcessor payPalProcessor,
            BankTransferProcessor bankTransferProcessor) {
        this.creditCardProcessor = creditCardProcessor;
        this.payPalProcessor = payPalProcessor;
        this.bankTransferProcessor = bankTransferProcessor;
    }

    @Override
    public PaymentProcessor create(PaymentMethod method) {
        return switch (method) {
            case CREDIT_CARD -> creditCardProcessor;
            case PAYPAL -> payPalProcessor;
            case BANK_TRANSFER -> bankTransferProcessor;
        };
    }
}

// ============================================================================
// PATTERN 5: Lazy Initialization
// ============================================================================

// @Service
public class ReportService {
    // Inject provider for lazy initialization
    // Spring: ObjectProvider<ExpensiveService>
    // Jakarta CDI: Instance<ExpensiveService>
    private final /* ObjectProvider<ExpensiveService> */ Object expensiveServiceProvider;

    public ReportService(/* ObjectProvider<ExpensiveService> */ Object expensiveServiceProvider) {
        this.expensiveServiceProvider = expensiveServiceProvider;
    }

    public Report generateReport(ReportType type) {
        // Service only created when needed
        // var service = expensiveServiceProvider.getIfAvailable();
        // return service != null ? service.generate(type) : Report.empty();
        return null; // Replace with actual implementation
    }
}

// ============================================================================
// PATTERN 6: Scope Management
// ============================================================================

// Request-scoped bean (new instance per HTTP request)
// @RequestScope
// @Component
public class RequestContext {
    private String correlationId;
    private String userId;

    public void initialize(String correlationId, String userId) {
        this.correlationId = correlationId;
        this.userId = userId;
    }

    public String getCorrelationId() { return correlationId; }
    public String getUserId() { return userId; }
}

// Prototype-scoped bean (new instance each time injected)
// @Scope("prototype")
// @Component
public class TransactionContext {
    private final String transactionId;

    public TransactionContext() {
        this.transactionId = java.util.UUID.randomUUID().toString();
    }

    public String getTransactionId() { return transactionId; }
}

// ============================================================================
// Stub interfaces for compilation (remove in actual usage)
// ============================================================================
interface UserRepository { Object save(Object user); }
interface EmailService {
    void sendWelcomeEmail(String email);
    void sendEmail(String to, String subject, String body);
}
interface UserMapper {
    Object toEntity(CreateUserRequest request);
    UserDto toDto(Object user);
}
record CreateUserRequest(String name, String email) {}
record UserDto(String id, String name, String email) {}
interface CacheManager {}
class CaffeineCacheManager implements CacheManager {}
class UserMapperImpl implements UserMapper {
    public Object toEntity(CreateUserRequest request) { return null; }
    public UserDto toDto(Object user) { return null; }
}
class SmtpEmailService implements EmailService {
    SmtpEmailService(EmailConfig config) {}
    public void sendWelcomeEmail(String email) {}
    public void sendEmail(String to, String subject, String body) {}
}
interface SmsGateway { void sendSms(String to, String message); }
interface PaymentProcessor {}
class CreditCardProcessor implements PaymentProcessor {}
class PayPalProcessor implements PaymentProcessor {}
class BankTransferProcessor implements PaymentProcessor {}
enum PaymentMethod { CREDIT_CARD, PAYPAL, BANK_TRANSFER }
record Report() { static Report empty() { return new Report(); } }
enum ReportType { DAILY, WEEKLY, MONTHLY }
