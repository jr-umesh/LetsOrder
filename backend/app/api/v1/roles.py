from app.models import UserRole

ROLE_POWER = {
    UserRole.MANAGER: 100,
    UserRole.COOK: 70,
    UserRole.WAITER: 60,
    UserRole.CUSTOMER: 40
}
